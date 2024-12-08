import os

from databricks.connect import DatabricksSession, cli
from databricks.sdk.config import Config
from pyspark.sql import SparkSession
from davidkhala.spark import SessionDecorator as SparkDecorator


class DatabricksConnect:

    @staticmethod
    def ping(serverless: bool = False):
        if serverless:
            os.environ['DATABRICKS_SERVERLESS_COMPUTE_ID'] = 'auto'
        cli.test()

    @staticmethod
    def get() -> SparkSession:
        _builder = DatabricksSession.builder
        try:
            return _builder.validateSession(True).getOrCreate()
        except Exception as e:
            if str(e) == 'Cluster id or serverless are required but were not specified.':
                return _builder.serverless(True).getOrCreate()
            else:
                raise e

    @staticmethod
    def from_servermore(config: Config) -> SparkSession:
        _builder = DatabricksSession.builder.validateSession(True)
        _builder.host(config.host)
        _builder.token(config.token)
        _builder.clusterId(config.cluster_id)
        return _builder.getOrCreate()

    @staticmethod
    def from_serverless(config: Config) -> SparkSession:
        # session validation flag is in vain. It will be overwritten
        # > Disable session validation for serverless
        _builder = DatabricksSession.builder
        _builder.host(config.host)
        _builder.token(config.token)
        _builder.serverless(True)
        return _builder.getOrCreate()


class SessionDecorator(SparkDecorator):
    @property
    def serverless(self) -> bool:
        # assert on serverless config
        return (
                self.conf.get("spark.databricks.clusterUsageTags.clusterId") is None
                and self.conf.get('spark.sql.ansi.enabled') == 'true'
                and self.conf.get('spark.sql.shuffle.partitions', ) == 'auto'
                and self.conf.__len__() == 2
        )

    @property
    def conf(self) -> dict:
        return self.spark.conf.getAll
