from typing import List, Dict, Any, Optional
from pymysql import connect
from pymysql.connections import Connection
from pymysql.cursors import Cursor

from spiderpy3.dbs.db import DB


class MysqlDB(DB):
    def __init__(
            self,
            *,
            host: str = "localhost",
            port: int = 3306,
            username: Optional[str] = None,
            password: Optional[str] = None,
            dbname: str,
            charset: str = "utf8mb4"
    ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dbname = dbname
        self.charset = charset

        super().__init__()

    @staticmethod
    def get_connection(
            *,
            host: str = "localhost",
            port: int = 3306,
            username: Optional[str] = None,
            password: Optional[str] = None,
            dbname: str,
            charset: str = "utf8mb4"
    ) -> Connection:
        connection = connect(
            user=username,
            password=password,
            host=host,
            database=dbname,
            port=port,
            charset=charset,
        )
        return connection

    @staticmethod
    def get_cursor(connection: Connection) -> Cursor:
        cursor = connection.cursor()
        return cursor

    def _open(self) -> None:
        self.connection = self.get_connection(host=self.host,
                                              port=self.port,
                                              username=self.username,
                                              password=self.password,
                                              dbname=self.dbname,
                                              charset=self.charset)
        self.cursor = self.get_cursor(self.connection)

    @staticmethod
    def close_cursor(cursor: Cursor) -> None:
        if cursor:
            cursor.close()

    @staticmethod
    def close_connection(connection: Connection) -> None:
        if connection:
            connection.close()

    def _close(self) -> None:
        self.close_cursor(self.cursor)
        self.close_connection(self.connection)

    def add(self) -> None:
        pass

    def delete(self) -> None:
        pass

    def update(self) -> None:
        pass

    def query(self, sql: str) -> List[Dict[str, Any]]:
        connection, cursor = self.connection, self.cursor

        cursor.execute(sql)
        result = cursor.fetchall()
        columns = [d[0] for d in cursor.description]
        rows = [dict(zip(columns, r)) for r in result]

        return rows
