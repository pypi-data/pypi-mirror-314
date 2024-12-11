from pyspark.sql import SparkSession

from davidkhala.databricks.connect import SessionDecorator
from davidkhala.databricks.workspace.path import API

class Index:
    notebook_name = "notebooks_dimension"

    def __init__(self, spark: SparkSession):
        self.spark = spark
        _d = SessionDecorator(spark)
        self.serverless = _d.serverless
        if self.serverless:
            self.schema = _d.schema

    @property
    def notebook_full_name(self):
        """
        full name of notebook dimension GlobalTempView or Table
        :return:
        """

        return f"{self.schema}.{self.notebook_name}" if self.serverless else f"global_temp.{self.notebook_name}"

    def build(self, api: API) -> bool:
        """
        :return: True if found any notebooks, False otherwise
        """
        _notebooks = api.scan_notebooks()
        if len(_notebooks) == 0:
            return False
        notebook_dataframe = self.spark.createDataFrame(_notebooks, ["object_id", "path"])
        if self.serverless:
            notebook_dataframe.writeTo(self.notebook_full_name).createOrReplace()
        else:
            notebook_dataframe.createOrReplaceGlobalTempView(self.notebook_name)
        return True

    def show(self):
        self.spark.sql(f"select * from {self.notebook_full_name}").show()

    def get_by(self, *, notebook_id: str = None, path: str = None):
        if self.spark.catalog.tableExists(self.notebook_full_name):
            if path:
                _any = self.spark.sql(
                    f"select object_id from {self.notebook_full_name} where path LIKE '%{path}%'").first()
                if _any:
                    return _any.object_id
            elif notebook_id:
                _any = self.spark.sql(
                    f"select path from {self.notebook_full_name} where object_id = {notebook_id}").first()
                if _any:
                    return _any.path

            else:
                raise "Either notebook_id or path is required"

        return