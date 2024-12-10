# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2023-08-30 14:20
# @Author : 毛鹏
import sqlite3

from mangokit import SQLiteConnect
from mangokit.enums.enums import CacheValueTypeEnum


class SqlCache:
    """ 文件缓存 """
    create_table_query1 = '''
    CREATE TABLE "test_data" (
      "id" INTEGER PRIMARY KEY AUTOINCREMENT,
      "key" TEXT NOT NULL,
      "value" TEXT,
      "case_id" TEXT,
      "type" INTEGER,
      "internal" INTEGER
    );
    '''

    def __init__(self, cache_path):
        self.cache_path = cache_path
        self.conn = SQLiteConnect(self.cache_path)
        for i in [self.create_table_query1]:
            try:
                self.conn.execute(i)
            except sqlite3.OperationalError:
                pass
        self.sql_statement_4 = f'INSERT INTO "test_data" ("key", "value", "type") VALUES (?, ?, ?);'
        self.sql_statement_5 = f'SELECT * FROM test_data WHERE `key` = ?'
        self.sql_statement_6 = f'DELETE FROM test_data WHERE `key` = ?'

    def get_sql_cache(self, key: str) -> str | list | dict | int | None:
        """
        获取缓存中指定键的值
        :param key: 缓存键
        :return:
        """
        res = self.conn.execute(self.sql_statement_5, (key,))
        if res:
            res = res[0]
        else:
            return None
        if res.get('type') == CacheValueTypeEnum.STR.value:
            return res.get('value')
        elif res.get('type') == CacheValueTypeEnum.INT.value:
            return int(res.get('value'))

    def set_sql_cache(self, key: str, value: str | list | dict, value_type: CacheValueTypeEnum = 0) -> None:
        """
        设置缓存键的值
        :param key: 缓存键
        :param value: 缓存值
        :param value_type: 值类型
        :return:
        """
        res2 = self.conn.execute(self.sql_statement_5, (key,))
        if res2:
            self.conn.execute(self.sql_statement_6, (key,))
        self.conn.execute(self.sql_statement_4, (key, value, value_type))

    @classmethod
    def delete_sql_cache(cls, key: str) -> None:
        """
        删除缓存中指定键的值
        :param key: 缓存键
        :return:
        """
        pass

    @classmethod
    def contains_sql_cache(cls, key: str) -> bool:
        """
        检查缓存中是否包含指定键
        :param key: 缓存键
        :return: 如果缓存中包含指定键，返回True；否则返回False
        """
        pass

    @classmethod
    def clear_sql_cache(cls) -> None:
        """
        清空缓存中的所有键值对
        :return:
        """
        pass
