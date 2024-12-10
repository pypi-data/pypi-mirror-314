import json
import os
import typing
from typing import Any, Dict, List, Optional, Tuple

import dbutils.pooled_db
import redis

from metasequoia_connector.connector import DSMetaConnector
from metasequoia_connector.connector.common import WrapConnector
from metasequoia_connector.connector.kafka import ConnKafkaConsumer
from metasequoia_connector.connector.mysql import MysqlConnectionPool, MysqlConnector
from metasequoia_connector.connector.ots import OTSConnector
from metasequoia_connector.connector.redis import RedisConnectionPool, RedisConnector
from metasequoia_connector.node import (DSMetaInstance, HiveInstance, KafkaServer, KafkaTopic, KafkaTopicsGroup,
                                        MysqlInstance, OTSInstance, RedisDatabase, RedisInstance, SshTunnel)

__all__ = ["ConnectManager"]

# 配置文件的默认环境变量名称
DEFAULT_METASEQUOIA_CONNECTOR_CONFIG_NAME = "METASEQUOIA_CONNECTOR_CONFIG"


# TODO 将配置输出到文件：https://www.cnblogs.com/wengzx/p/18019494


class ConnectManager:
    """连接管理器"""

    ENCODING = "UTF-8"  # 编码格式

    def __init__(self, configuration: Dict[str, Any], mode: str = "dev"):
        self._configuration = configuration
        self._mode = mode

        # 缓存的连接池
        self._redis_pool_dict: Dict[str, RedisConnectionPool] = {}
        self._mysql_pool_dict: Dict[Tuple[str, Optional[str]], MysqlConnectionPool] = {}
        self._ots_conn_dict: Dict[str, OTSConnector] = {}

    @classmethod
    def from_config_file(cls, config_path: str, mode: str = "dev") -> "ConnectManager":
        """根据配置文件路径，并加载配置文件"""
        with open(config_path, "r", encoding=ConnectManager.ENCODING) as file:
            configuration = json.load(file)
        return ConnectManager(
            configuration=configuration,
            mode=mode
        )

    @classmethod
    def from_environment(cls, environ_name: Optional[str] = None, mode: str = "dev") -> "ConnectManager":
        """从环境变量中读取配置文件路径，并加载配置文件

        Parameters
        ----------
        environ_name : Optional[str], default = None
            环境变量名称，如果为空则使用默认名称
        mode : str, default = "dev"
            使用模式（会根据模式读取配置文件中的配置信息）
        """
        # 从环境变量中读取文件路径
        if environ_name is None:
            environ_name = DEFAULT_METASEQUOIA_CONNECTOR_CONFIG_NAME
        config_path = os.environ.get(environ_name)

        # 加载配置文件
        with open(config_path, "r", encoding=ConnectManager.ENCODING) as file:
            configuration = json.load(file)

        return ConnectManager(
            configuration=configuration,
            mode=mode
        )

    def __hash__(self):
        return self.get_hash(self._configuration)

    @staticmethod
    def get_hash(obj: object):
        if isinstance(obj, dict):
            return hash(tuple([(key, ConnectManager.get_hash(value)) for key, value in obj.items()]))
        if isinstance(obj, list):
            return hash(tuple([ConnectManager.get_hash(elem) for elem in obj]))
        return hash(obj)

    def __eq__(self, other: str) -> bool:
        if not isinstance(other, ConnectManager):
            return False
        return self._configuration == other._configuration

    # ------------------------------ 读取 MySQL 相关配置 ------------------------------

    def mysql_list(self) -> List[str]:
        """获取 MySQL 列表"""
        return self._get_name_list("MySQL")

    def mysql_dict(self, mysql_name: str) -> Dict[str, Any]:
        """获取 MySQL 信息"""
        return self._confirm_params(
            section="MySQL",
            config=self._get_section("MySQL", mysql_name),
            params=["host", "port", "user", "passwd"]
        )

    def mysql_obj(self, name: str) -> MysqlInstance:
        """获取 MysqlInstance 对象"""
        mysql_info = self.mysql_dict(name)
        ssh_tunnel = self.ssh_tunnel_obj(mysql_info["use_ssh"]) if mysql_info.get("use_ssh") else None
        return MysqlInstance(host=mysql_info["host"],
                             port=mysql_info["port"],
                             user=mysql_info["user"],
                             passwd=mysql_info["passwd"],
                             ssh_tunnel=ssh_tunnel)

    def mysql_refer_name(self, name: str) -> str:
        """获取 MySQL 的名称"""
        return self._configuration["MySQL"][name].get("_name", "")

    def mysql_refer_type(self, name: str) -> str:
        """获取 MySQL 的类型"""
        return self._configuration["MySQL"][name].get("_type", "")

    def mysql_refer_type_enum(self):
        """获取 MySQL 的 _type 属性的枚举值"""
        return {self.mysql_refer_type(mysql_name) for mysql_name in self.mysql_list()}

    def mysql_start_pool(self, mysql_name: str, schema_name: Optional[str] = None) -> MysqlConnectionPool:
        """根据 MySQL 的配置项名称，创建连接池

        Parameters
        ----------
        mysql_name : str
            MySQL 配置项的名称
        schema_name : Optional[str] = None
            数据库名称

        Returns
        -------
        MysqlConnectionPool
            MySQL 连接池对象
        """
        if (mysql_name, schema_name) in self._mysql_pool_dict:
            raise KeyError(f"重复启动 MySQL 连接池: ({mysql_name}, {schema_name})")
        mysql_instance = self.mysql_obj(mysql_name)
        self._mysql_pool_dict[(mysql_name, schema_name)] = MysqlConnectionPool(mysql_instance=mysql_instance,
                                                                               schema=schema_name)
        return self._mysql_pool_dict[(mysql_name, schema_name)]

    def mysql_close_pool(self, mysql_name: str, schema_name: Optional[str] = None) -> None:
        """根据 MySQL 的配置项名称，关闭连接池"""
        if (mysql_name, schema_name) not in self._mysql_pool_dict:
            raise KeyError(f"要关闭的 MySQL 连接池不存在: ({mysql_name}, {schema_name})")
        self._mysql_pool_dict[(mysql_name, schema_name)].close()  # 关闭连接池
        del self._mysql_pool_dict[(mysql_name, schema_name)]  # 从缓存连接池中移除连接池

    def mysql_connect(self, mysql_name: str, schema_name: Optional[str] = None, use_pool: bool = True):
        """根据 MySQL 配置项中名称，获取连接（当 use_pool 为 True 时，从连接池中获取；否则，创建新连接）"""
        if use_pool is True:
            if (mysql_name, schema_name) not in self._mysql_pool_dict:
                self.mysql_start_pool(mysql_name, schema_name)
            connection_pool = self._mysql_pool_dict[(mysql_name, schema_name)]
            connection_pool = typing.cast(dbutils.pooled_db.PooledDB, connection_pool)
            return WrapConnector(connection_pool.connection())
        return MysqlConnector(mysql_instance=self.mysql_obj(mysql_name), schema=schema_name)

    def mysql_new_connect(self, name: str, schema_name: Optional[str] = None):
        """根据实例名称，创建 MySQL 连接器"""
        return MysqlConnector(mysql_instance=self.mysql_obj(name), schema=schema_name)

    # ------------------------------ 读取 Ssh_Tunnel 相关配置 ------------------------------

    def ssh_tunnel_list(self):
        """获取 SSH 列表"""
        return self._get_name_list("Ssh_Tunnel")

    def ssh_tunnel_dict(self, ssh_tunnel_name: str) -> Dict[str, Any]:
        """获取 SSH 信息"""
        return self._confirm_params(
            section="Ssh_Tunnel",
            config=self._get_section("Ssh_Tunnel", ssh_tunnel_name),
            params=["host", "port"]
        )

    def ssh_tunnel_obj(self, ssh_tunnel_name: str) -> SshTunnel:
        """获取 SshTunnel 对象"""
        ssh_info = self.ssh_tunnel_dict(ssh_tunnel_name)
        return SshTunnel(host=ssh_info["host"],
                         port=ssh_info["port"],
                         username=ssh_info["username"],
                         password=ssh_info.get("password"),
                         pkey=ssh_info.get("pkey"))

    # ------------------------------ 读取 Kafka 相关配置 ------------------------------

    def kafka_list(self) -> List[str]:
        """获取 Kafka 列表"""
        return self._get_name_list("Kafka")

    def kafka_dict(self, name: str) -> Dict[str, Any]:
        return self._confirm_params(
            section="Kafka",
            config=self._get_section("Kafka", name),
            params=["bootstrap_servers"]
        )

    def kafka_obj(self, name: str) -> KafkaServer:
        """获取 Kafka Servers 对象"""
        kafka_info = self.kafka_dict(name)
        ssh_tunnel = self.ssh_tunnel_obj(kafka_info["use_ssh"]) if kafka_info.get("use_ssh") else None
        return KafkaServer(bootstrap_servers=kafka_info["bootstrap_servers"],
                           ssh_tunnel=ssh_tunnel)

    # ------------------------------ 读取 Kafka_Topic 相关配置 ------------------------------
    def kafka_topic_list(self) -> List[str]:
        """读取 Kafka-TOPIC 的配置列表"""
        return self._get_name_list("Kafka_Topic")

    def kafka_topic_dict(self, kafka_topic_name: str) -> Dict[str, Any]:
        """获取 Kafka-TOPIC 配置项的信息"""
        return self._confirm_params(
            section="Kafka_Topic",
            config=self._get_section("Kafka_Topic", kafka_topic_name),
            params=["kafka_server", "topic"]
        )

    def kafka_topic_obj(self, kafka_topic_name: str) -> KafkaTopic:
        """根据 Kafka-TOPIC 配置项的信息，构造 KafkaTopic 对象"""
        kafka_topic_info = self.kafka_topic_dict(kafka_topic_name)
        kafka_server = self.kafka_obj(kafka_topic_info["kafka_server"])
        return KafkaTopic(
            kafka_server=kafka_server,
            topic=kafka_topic_info["topic"]
        )

    # ------------------------------ 读取 Kafka_Topics_Group 相关配置 ------------------------------
    def kafka_topics_group_list(self) -> List[str]:
        """读取 Kafka_Topics_Group 的配置列表"""
        return self._get_name_list("Kafka_Topics_Group")

    def kafka_topics_group_dict(self, kafka_topics_group_name: str) -> Dict[str, Any]:
        """获取 Kafka_Topics_Group 配置项的信息"""
        return self._confirm_params(
            section="Kafka_Topics_Group",
            config=self._get_section("Kafka_Topics_Group", kafka_topics_group_name),
            params=["kafka_server", "topics", "group_id"]
        )

    def kafka_topics_group_obj(self, kafka_topics_group_name: str) -> KafkaTopicsGroup:
        """根据 Kafka-TOPIC 配置项的信息，构造 KafkaTopic 对象"""
        kafka_topic_group_info = self.kafka_topics_group_dict(kafka_topics_group_name)
        kafka_server = self.kafka_obj(kafka_topic_group_info["kafka_server"])
        return KafkaTopicsGroup(
            kafka_server=kafka_server,
            topics=kafka_topic_group_info["topics"],
            group_id=kafka_topic_group_info["group_id"]
        )

    def kafka_topics_group_new_consumer(self, kafka_topics_group_name: str) -> ConnKafkaConsumer:
        """根据 Kafka_Topic_Group 的名称，启动 KafkaConsumer 连接器"""
        kafka_topic_group = self.kafka_topics_group_obj(kafka_topics_group_name)
        return ConnKafkaConsumer.by_kafka_topic_group(kafka_topic_group)

    # ------------------------------ 读取 Hive 相关配置 ------------------------------

    def hive_list(self) -> List[str]:
        """获取 Hive 列表"""
        return self._get_name_list("Hive")

    def hive_dict(self, name: str) -> Dict[str, Any]:
        return self._confirm_params("Hive", self._get_section("Hive", name),
                                    ["hosts", "port"])

    def hive_obj(self, name: str) -> HiveInstance:
        """获取 Hive 列表"""
        hive_info = self.hive_dict(name)
        ssh_tunnel = self.ssh_tunnel_obj(hive_info["use_ssh"]) if hive_info.get("use_ssh") else None
        return HiveInstance(hosts=hive_info["hosts"], port=hive_info["port"], username=hive_info.get("username"),
                            ssh_tunnel=ssh_tunnel)

    # ------------------------------ 读取 DolphinScheduler 相关配置 ------------------------------

    def dolphin_meta_list(self) -> List[str]:
        """获取海豚调度元数据清单"""
        return self._get_name_list("DolphinMeta")

    def dolphin_meta_dict(self, name: str) -> Dict[str, Any]:
        """获取海豚调度元数据信息"""
        return self._confirm_params("DolphinMeta", self._get_section("DolphinMeta", name),
                                    ["host", "port", "user", "passwd"])

    def dolphin_meta_obj(self, name: str) -> DSMetaInstance:
        """获取海豚调度元数据的 DolphinMetaInstance 对象"""
        dolphin_meta_info = self.dolphin_meta_dict(name)
        ssh_tunnel = self.ssh_tunnel_obj(dolphin_meta_info["use_ssh"]) if dolphin_meta_info.get("use_ssh") else None
        return DSMetaInstance(
            host=dolphin_meta_info["host"],
            port=dolphin_meta_info["port"],
            user=dolphin_meta_info["user"],
            passwd=dolphin_meta_info["passwd"],
            db=dolphin_meta_info["db"],
            ssh_tunnel=ssh_tunnel
        )

    def dolphin_meta_new_connect(self, name: str):
        """根据海豚元数据名称，创建海豚元数据连接器"""
        dolphin_meta_instance = self.dolphin_meta_obj(name)
        return DSMetaConnector(dolphin_scheduler_meta_info=dolphin_meta_instance)

    # ------------------------------ 读取 OTS 相关配置 ------------------------------

    def ots_list(self) -> List[str]:
        """获取 OTS 元数据清单"""
        return self._get_name_list("OTS")

    def ots_dict(self, name: str) -> Dict[str, Any]:
        """获取 OTS 元数据信息"""
        return self._confirm_params("OTS", self._get_section("OTS", name),
                                    ["end_point", "access_key_id", "access_key_secret", "instance_name"])

    def ots_obj(self, name: str) -> OTSInstance:
        """获取 OTS 元数据的 OTSInstance 对象"""
        ots_info = self.ots_dict(name)
        return OTSInstance(
            end_point=ots_info["end_point"],
            access_key_id=ots_info["access_key_id"],
            access_key_secret=ots_info["access_key_secret"],
            instance_name=ots_info["instance_name"]
        )

    def otssql_connect(self, ots_name: str, use_pool: bool = True, **params):
        """根据 OTS 配置项中名称，获取连接（当 use_pool 为 True 时，从连接池中获取；否则，创建新连接）

        TODO 待支持实际的连接池
        """
        if use_pool is False:
            return OTSConnector(ots_instance=self.ots_obj(ots_name))
        if ots_name not in self._ots_conn_dict:
            self._ots_conn_dict[ots_name] = OTSConnector(ots_instance=self.ots_obj(ots_name), **params)
        return self._ots_conn_dict[ots_name]

    def otssql_new_connect(self, ots_name: str, **params):
        """根据实例名称，创建 MySQL 连接器"""
        return OTSConnector(ots_instance=self.ots_obj(ots_name), **params)

    # ------------------------------ 读取 Redis 相关配置 ------------------------------

    def redis_list(self) -> List[str]:
        """获取 Redis 元数据清单"""
        return self._get_name_list("Redis")

    def redis_dict(self, name: str) -> Dict[str, Any]:
        """获取 Redis 实例信息"""
        return self._confirm_params("Redis", self._get_section("Redis", name),
                                    ["host", "passwd", "port"])

    def redict_obj(self, name: str) -> RedisInstance:
        """获取 RedisInstance 对象"""
        redis_info = self.redis_dict(name)
        ssh_tunnel = self.ssh_tunnel_obj(redis_info["use_ssh"]) if redis_info.get("use_ssh") else None
        return RedisInstance(
            host=redis_info["host"],
            passwd=redis_info["passwd"],
            port=redis_info["port"],
            ssh_tunnel=ssh_tunnel
        )

    def redis_new_connect(self, name: str, db: int) -> RedisConnector:
        """根据 Redis 实例名称和数据库创建 Redis 连接"""
        redis_instance = self.redict_obj(name)
        return RedisConnector(RedisDatabase(instance=redis_instance, db=db))

    # ------------------------------ 读取 Redis_Database 相关配置 ------------------------------

    def redis_database_list(self):
        """获取 Redis_Database 清单"""
        return self._get_name_list("Redis_Database")

    def redis_database_dict(self, redis_database_name: str):
        """根据 Redis_Database 的配置项名称，获取 Redis_Database 信息"""
        return self._confirm_params(
            section="Redis_Database",
            config=self._get_section("Redis_Database", redis_database_name),
            params=["instance", "db"]
        )

    def redis_database_obj(self, redis_database_name: str) -> RedisDatabase:
        """根据 Redis_Database 的配置项名称，构造 RedisDatabase 对象"""
        redis_database_info = self.redis_database_dict(redis_database_name)
        redis_instance = self.redict_obj(redis_database_info["instance"])
        return RedisDatabase(instance=redis_instance, db=redis_database_info["db"])

    def redis_database_start_pool(self, redis_database_name: str) -> RedisConnectionPool:
        """根据 Redis_Database 的配置项名称，创建连接池

        Parameters
        ----------
        redis_database_name : str
            Redis_Database 配置项的名称

        Returns
        -------
        RedisConnectionPool
            Redis 连接池对象
        """
        if redis_database_name in self._redis_pool_dict:
            raise KeyError(f"重复启动 Redis_Database 连接池: {redis_database_name}")
        redis_database_obj = self.redis_database_obj(redis_database_name)
        self._redis_pool_dict[redis_database_name] = RedisConnectionPool(redis_database_obj)
        return self._redis_pool_dict[redis_database_name]

    def redis_database_close_pool(self, redis_database_name: str) -> None:
        """根据 Redis_Database 的配置项名称，关闭连接池"""
        if redis_database_name not in self._redis_pool_dict:
            raise KeyError(f"要关闭的 Redis_Database 连接池不存在: {redis_database_name}")
        self._redis_pool_dict[redis_database_name].close()  # 关闭连接池
        del self._redis_pool_dict[redis_database_name]  # 从缓存连接池中移除连接池

    def redis_database_connect(self, redis_database_name: str, use_pool: bool = True):
        """根据 Redis_Database 配置项中名称，获取连接（当 use_pool 为 True 时，从连接池中获取；否则，创建新连接）"""
        if use_pool is True:
            if redis_database_name not in self._redis_pool_dict:
                self.redis_database_start_pool(redis_database_name)
            connection_pool = self._redis_pool_dict[redis_database_name]
            connection_pool = typing.cast(redis.ConnectionPool, connection_pool)
            return redis.Redis(connection_pool=connection_pool)
        return RedisConnector(self.redis_database_obj(redis_database_name))

    def redis_database_new_connect(self, name: str):
        """根据 Redis_Database 配置项中的名称创建 Redis 连接"""
        return RedisConnector(self.redis_database_obj(name))

    # ---------- 其他工具方法 ----------

    def _get_name_list(self, section: str):
        """获取每种配置项中的所有名称的列表"""
        if section not in self._configuration:
            return []
        return list(self._configuration[section])

    def _get_section(self, section: str, name: str) -> Dict[str, Any]:
        """获取每种类型的配置信息数据"""
        if section not in self._configuration or name not in self._configuration[section]:
            return {}
        config = self._configuration[section][name].get("mode:common", {}).copy()  # 先加载通用配置
        config.update(self._configuration[section][name].get(f"mode:{self._mode}", {}))  # 然后再加对应模式的配置
        return config

    @staticmethod
    def _confirm_params(section: str, config: Dict[str, Any], params: List[str]) -> Dict[str, Any]:
        """检查参数是否满足"""
        for param in params:
            assert param in config, f"param {param} not in {section} config"
        return config

    @classmethod
    def make_templates(cls, path: str):
        """在指定路径下生成模板配置文件"""
        if os.path.exists(path):
            raise ValueError(f"配置文件已存在({path}),创建模板文件失败!")
        with open(path, "w", encoding=cls.ENCODING) as file:
            file.write(json.dumps(
                {"MySQL": {"localhost": {"host": "localhost", "port": 3306, "user": "root", "passwd": "123456"}},
                 "SSH": {"demo": {"host": "...", "port": "...", "username": "...", "pkey": "..."}}}))
            print("配置文件模板生成完成")

    def close(self, is_del: bool = False):
        """关闭连接管理器中的所有连接、连接池

        Parameters
        ----------
        is_del : bool, default = False
            是否是在对象销毁的过程中调用：如果是在对象销毁的过程中调用，则不销毁 SshTunnel 对象，因为该对象在销毁过程中调用 close 方法可能出现
            无法预料的报错或卡死
        """
        # 关闭 Redis 连接池
        for redis_connection_pool in self._redis_pool_dict.values():
            redis_connection_pool.close(is_del=True)

        # 关闭 MySQL 连接池
        for mysql_connection_pool in self._mysql_pool_dict.values():
            mysql_connection_pool.close(is_del=True)

    def __del__(self):
        """在对象被销毁时调用"""
        self.close(is_del=True)
