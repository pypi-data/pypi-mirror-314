import os

from davidkhala.syntax.fs import read

from davidkhala.databricks.workspace.warehouse import Warehouse


class Query:
    pwd = os.path.dirname(__file__)

    def __init__(self, w: Warehouse):
        self.w = w

    def tables(self):
        return self.w.run(read(os.path.join(self.pwd, 'Table.sql')))

    def columns(self):
        return self.w.run(read(os.path.join(self.pwd, 'Column.sql')))
