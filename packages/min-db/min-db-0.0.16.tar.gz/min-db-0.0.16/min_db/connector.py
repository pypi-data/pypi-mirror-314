from typing import Optional, Generator

import oracledb
from mysql.connector import pooling

from min_db.mapper import Mapper
from min_db.types import DB_INFO, DB_TYPE


class Connector:
    def __init__(self, db_type: str, ip: str, port: int, user: str, password: str, db: str | None = None,
                 sid: str | None = None, dsn: str | None = None, query_path: str | None = None,
                 collation: Optional[str] = None,
                 session_pool_min: int = 5, session_pool_max: int = 10):
        if db_type == DB_TYPE.ORACLE:
            if sid is None:
                raise AttributeError("sid must be defined on oracle")
        if db_type == DB_TYPE.MYSQL:
            if db is None:
                raise AttributeError("db must be defined on oracle")
        self._db_info = DB_INFO(type=db_type, sid=sid, db=db, user=user,
                                password=password, ip=ip, port=port,
                                session_pool_min=session_pool_min, session_pool_max=session_pool_max)
        if query_path is not None:
            self._mapper = Mapper(path=query_path)
        else:
            self._mapper = None
        self._session_pool: oracledb.SessionPool | pooling.MySQLConnectionPool | None = None
        if db_type == DB_TYPE.ORACLE:
            if dsn in None:
                self._dsn = oracledb.makedsn(host=ip, port=port, sid=sid)
            else:
                self._dsn = dsn
            self._session_pool = oracledb.SessionPool(user=user, password=password, dsn=self._dsn,
                                                      min=session_pool_min, max=session_pool_max,
                                                      increment=1, encoding="UTF-8")
        elif db_type == DB_TYPE.MYSQL:
            mysql_kwargs = {"pool_name": "pool_mysql",
                            "pool_size": session_pool_max,
                            "pool_reset_session": True,
                            "host": ip,
                            "port": port,
                            "database": db,
                            "user": user,
                            "password": password}
            if collation is not None:
                mysql_kwargs["collation"] = collation
            self._session_pool = pooling.MySQLConnectionPool(**mysql_kwargs)

    def connection_test(self) -> None:
        try:
            if self._db_info.type == DB_TYPE.MYSQL:
                test_connection = self._session_pool.get_connection()
                print(test_connection.get_server_info())
                test_connection.close()
            elif self._db_info.type == DB_TYPE.ORACLE:
                test_connection = self._session_pool.acquire()
                self._session_pool.release(test_connection)
        except Exception as exc:
            raise exc
        else:
            print("success")

    def select_one(self, query: Optional[str] = None, namespace: Optional[str] = None, query_id: Optional[str] = None,
                   param: Optional[dict] = None):
        if query is None:
            query = self._mapper.get_query(namespace, query_id, param)
        print(query)
        if self._db_info.type == DB_TYPE.MYSQL:
            with self._session_pool.get_connection() as connection_obj:
                cursor = connection_obj.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                cursor.close()
                return result
        elif self._db_info.type == DB_TYPE.ORACLE:
            with self._session_pool.acquire() as connection_obj:
                cursor = connection_obj.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                cursor.close()
                return result

    def select(self, query: Optional[str] = None, namespace: Optional[str] = None, query_id: Optional[str] = None,
               param: Optional[dict] = None):
        if query is None:
            query = self._mapper.get_query(namespace, query_id, param)
        print(query)
        if self._db_info.type == DB_TYPE.MYSQL:
            with self._session_pool.get_connection() as connection_obj:
                cursor = connection_obj.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                return result
        elif self._db_info.type == DB_TYPE.ORACLE:
            with self._session_pool.acquire() as connection_obj:
                cursor = connection_obj.cursor()
                result = cursor.execute(query)
                result = result.fetchall()
                cursor.close()
                return result

    def select_chunk(self, query: Optional[str] = None, namespace: Optional[str] = None, query_id: Optional[str] = None,
                     param: Optional[dict] = None, prefetch_row: Optional[int] = 10000,
                     array_size: Optional[int] = 10000,
                     include_headers: bool = False) -> Generator[list | tuple, None, None]:
        if query is None:
            query = self._mapper.get_query(namespace, query_id, param)
        if self._db_info.type == DB_TYPE.ORACLE:
            with self._session_pool.acquire() as conn:
                chunk_cursor = conn.cursor()
                if prefetch_row is not None:
                    chunk_cursor.prefetchrows = prefetch_row
                if array_size is not None:
                    chunk_cursor.arraysize = array_size
                chunk_cursor.execute(query)
                if include_headers:
                    col_names = tuple(row[0] for row in chunk_cursor.description)
                    yield col_names
                while True:
                    results = chunk_cursor.fetchmany(array_size)
                    if not results:
                        break
                    yield results
                chunk_cursor.close()
        elif self._db_info.type == DB_TYPE.MYSQL:
            with self._session_pool.get_connection() as connection_obj:
                cursor = connection_obj.cursor()
                cursor.execute(query)
                if include_headers:
                    yield cursor.column_names
                while True:
                    result = cursor.fetchmany(array_size)
                    if not result:
                        break
                    yield result
                cursor.close()
                # res = []
                # for row in cursor:
                #     res += row
                #     if len(res) >= array_size:
                #         yield res
                #         res = []
                # if res:
                #     yield res

    def execute(self, namespace: str, query_id: str, param: dict = None):
        query = self._mapper.get_query(namespace, query_id, param)
        print(query)
        if self._db_info.type == DB_TYPE.ORACLE:
            with self._session_pool.acquire() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                print("commit: ", cursor.rowcount)
                cursor.close()
                return
        elif self._db_info.type == DB_TYPE.MYSQL:
            with self._session_pool.get_connection() as connection_obj:
                cursor = connection_obj.cursor()
                cursor.execute(query)
                connection_obj.commit()
                print("commit: ", cursor.rowcount)
                cursor.close()
                return
            # with self._session_pool.get_connection() as conn:
            #     cursor = conn.cursor()
            #     cursor.execute(query)
            #     conn.commit()
            #     print("commit: ", cursor.rowcount)
            #     cursor.close()
            #     return

    def multiple_execution(self, queries: list[dict]):
        num_queries = len(queries)
        if self._db_info.type == DB_TYPE.ORACLE:
            raise RuntimeError("ORACLE not supported currently.")
        elif self._db_info.type == DB_TYPE.MYSQL:
            with self._session_pool.get_connection() as connection_obj:
                cursor = connection_obj.cursor()
                for idx, query in enumerate(queries):
                    if "param" in query:
                        query = self._mapper.get_query(query["namespace"], query["query_id"], query["param"])
                    else:
                        query = self._mapper.get_query(query["namespace"], query["query_id"])
                    print(f"multiple execution: {idx + 1}/{num_queries}\n"
                          f"{query}")
                    cursor.execute(query)
                connection_obj.commit()
                print("commit: ", cursor.rowcount)
                cursor.close()
                return
