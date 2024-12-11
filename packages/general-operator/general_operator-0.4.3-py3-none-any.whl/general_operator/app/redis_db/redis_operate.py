import functools
import json
from typing import Any
import re
from redis import RedisError
from .function import OperateFunction
import redis
from fastapi.encoders import jsonable_encoder
from enum import Enum


class RedisOperate(OperateFunction):
    def __init__(self, redis_db: redis.Redis, exc):
        self.redis = redis_db
        self.exc = exc

    @staticmethod
    def exception_handler(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RedisError as e:
                pattern = r"Error (\d+)"
                match = re.search(pattern, e.args[0])
                if match:
                    error_code = match.group(1)
                    raise self.exc(status_code=487, message=e, message_code=int(error_code))
                else:
                    raise self.exc(status_code=487, message=e, message_code=3)
            except json.JSONDecodeError:
                raise self.exc(status_code=487, message="redis operation json decode error", message_code=4)
            except self.exc as e:
                raise e
            except Exception as e:
                raise self.exc(status_code=487, message=e, message_code=999)

        return wrapper

    @exception_handler
    def clean_redis_by_name(self, table_name):
        if self.redis.exists(table_name):
            if self.redis.delete(table_name) == 1:
                print(f"clean redis table: {table_name}")

    @exception_handler
    def write_to_redis(self, table_name: str, key: str | None = None,
                       value: str | int | None = None, mapping: dict | None = None, items: list | None = None):
        self.redis.hset(table_name, key, value, mapping, items)

    @exception_handler
    def write_sql_data_to_redis(self, table_name: str,
                                sql_data_list: list, schemas_model,
                                key: str = "id") -> list:
        """
        :param table_name:
        :param sql_data_list:
        :param schemas_model:
        :param key:
        :return:
        """
        if not sql_data_list:
            return list()
        result: list[Any] = list()
        # 將要寫入redis的資料
        set_mapping: dict = dict()
        if key == "id":
            result = self.write_main_table(sql_data_list, schemas_model, set_mapping)
        else:
            result = self.write_index_table(sql_data_list, schemas_model, set_mapping, key, table_name, self.redis)
        if set_mapping:
            self.redis.hset(table_name, mapping=set_mapping)

    @exception_handler
    def read_redis_return_dict(self, table_name: str, key_set: set) -> dict:
        if not key_set:
            return dict()
        key_list = list(key_set)
        raw_data = self.redis.hmget(table_name, key_list)
        return {key: json.loads(data.decode("utf-8")) for key, data in zip(key_list, raw_data) if data is not None}

    @exception_handler
    def read_redis_all_data(self, table_name: str) -> list[dict]:
        result = []
        for datum in self.redis.hvals(table_name):
            result.append(json.loads(datum))
        return result

    @exception_handler
    def read_redis_data_without_exception(self, table_name: str, key_set: set) -> list:
        if not key_set:
            return list()
        raw_data = self.redis.hmget(table_name, list(key_set))
        return [json.loads(data) for data in raw_data if data is not None]

    @exception_handler
    def read_redis_data(self, table_name: str, key_set: set) -> list:
        if not key_set:
            return list()
        raw_data = self.redis.hmget(table_name, list(key_set))
        if None in raw_data:
            raise self.exc(status_code=487, message=f"id:{key_set} is not exist", message_code=1)
        return [json.loads(data) for data in raw_data]

    @exception_handler
    def delete_redis_data(self, table_name: str, data_list: list, schemas_model,
                          key: str = "id", update_list: list = None) -> str:
        """

        :param table_name:
        :param data_list:
        :param schemas_model:
        :param key:
        :param update_list: 如果是因為update sql table需要刪除redis，要加此參數
        :return:
        """
        p = self.redis.pipeline()
        update_dict = dict()
        is_update = True
        if update_list is None:
            is_update = False
            update_list = list()
        for update_data in update_list:
            update_dict[update_data.id] = update_data
        for data in data_list:
            row = schemas_model(**jsonable_encoder(data))
            # 刪除主表
            if key == "id":
                p.hdel(table_name, getattr(row, key))
                continue

            # 刪除附表(index table)
            is_complex_key = False
            has_key = False
            key_list = []
            if len(key.split("__")) > 1:
                is_complex_key = True
                key_list = key.split("__")

            #  判斷更新資料有沒有此key
            if is_complex_key:
                key_list = key.split("__")
                for k in key_list:
                    if getattr(update_dict.get(row.id, None), k, None) is not None:
                        has_key = True
                        break
            else:
                if getattr(update_dict.get(row.id, None), key, None) is not None:
                    has_key = True
            # 是 (update且有key的情況) 或 單純刪除表
            if (is_update and has_key) or not is_update:
                # key是complex的情況
                if is_complex_key:
                    complex_value = ""
                    for k in key_list:
                        value = getattr(row, k)
                        if value is not None:
                            if isinstance(value, Enum):
                                complex_value += value.value
                            else:
                                complex_value += str(value)
                    id_list = json.loads(self.redis.hget(table_name, complex_value))
                    id_list.remove(row.id)
                    if not id_list:
                        p.hdel(table_name, complex_value)
                    else:
                        p.hset(table_name, complex_value, json.dumps(id_list))

                # sql type 是 json list的情況
                elif isinstance(getattr(row, key), list):
                    for value in getattr(row, key):
                        id_list = json.loads(self.redis.hget(table_name, value))
                        id_list.remove(row.id)
                        if not id_list:
                            p.hdel(table_name, value)
                        else:
                            p.hset(table_name, value, json.dumps(id_list))

                # sql type 是單一值的情況
                else:
                    value = getattr(row, key)
                    # key可能為空值得情況
                    if value is not None:
                        id_list = json.loads(self.redis.hget(table_name, value))
                        id_list.remove(row.id)
                        if not id_list:
                            p.hdel(table_name, value)
                        else:
                            p.hset(table_name, value, json.dumps(id_list))
        p.execute()
        return "Ok"
