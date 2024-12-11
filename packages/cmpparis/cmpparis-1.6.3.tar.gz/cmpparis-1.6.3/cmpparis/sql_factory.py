class SqlFactory:
    @staticmethod
    def create_sql_connector(connector_type, server, database, username, password):
        if connector_type == "odbc":
            from .odbc import Odbc

            return Odbc(server, database, username, password)
        elif connector_type == "mssql":
            from .mssql import Mssql

            return Mssql(server, database, username, password)
        else:
            raise ValueError("Invalid connector type")