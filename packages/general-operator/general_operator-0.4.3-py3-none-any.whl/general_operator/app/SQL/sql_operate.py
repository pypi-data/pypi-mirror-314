import functools
import psycopg2
import pymysql
from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError
from ...function.encoder import custom_jsonable_encoder

class SQLOperate:
    def __init__(self, exc):
        self.exc = exc
        self.null_set = {-999999, "null"}


    @staticmethod
    def exception_handler(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except DBAPIError as e:
                if isinstance(e.orig, psycopg2.Error):
                    pg_error = e.orig
                    if pg_error.pgerror:
                        message = pg_error.pgerror.replace("\n", " ").replace("\r", " ")
                    else:
                        message = str(pg_error).replace("\n", " ").replace("\r", " ")
                    if pg_error.pgcode:
                        code = pg_error.pgcode
                    else:
                        code = 1
                        message = "postgres connection error: " + message
                    raise self.exc(status_code=489, message=message, message_code=code)
                elif isinstance(e.orig, pymysql.Error):
                    code, msg = e.orig.args
                    raise self.exc(status_code=486, message=msg, message_code=code)
            except UnmappedInstanceError:
                raise self.exc(status_code=486, message=f"id: one or more of ids is not exist",
                               message_code=2)
        return wrapper

    @exception_handler
    def create_multiple_sql_data(self, db: Session, create_list: list, sql_model) -> list:
        add_list = list()
        for datum in create_list:
            if isinstance(datum, dict):
                add_list.append(sql_model(**datum))
            elif isinstance(datum, BaseModel):
                try:
                    # pydantic 2.x.x version
                    add_list.append(sql_model(**datum.model_dump()))
                except Exception as e:
                    # pydantic 1.x.x version
                    print(e)
                    add_list.append(sql_model(**datum.dict()))
        db.add_all(add_list)
        db.flush()
        result = list()
        for datum in add_list:
            db.refresh(datum)
            result.append(datum)
        return result

    @exception_handler
    def get_sql_data(self, db: Session, sql_model, field_value_set: set,
                     sql_field: str = "id", check_data_list: bool = True) -> list:
        data_list = db.query(sql_model).filter(getattr(sql_model, sql_field).in_(field_value_set)).all()
        if not data_list and check_data_list:
            raise self.exc(status_code=486, message=f"one or more {sql_field} value are not in {field_value_set}",
                           message_code=3)
        return data_list

    @exception_handler
    def get_all_sql_data(self, db: Session, sql_model) -> list:
        skip: int = 0
        limit: int = 500
        result = list()
        while True:
            d = db.query(sql_model).offset(skip).limit(limit).all()
            if len(d) > 0:
                result.extend(d)
                skip += limit
            else:
                break
        return [custom_jsonable_encoder(i, 8) for i in result]

    @exception_handler
    def update_multiple_sql_data(self, db: Session, update_list: list, sql_model):
        update_data_dict = dict()
        update_data_id_set = set()
        if not update_list:
            return []
        for update_data in update_list:
            update_data_dict[update_data.id] = update_data
            update_data_id_set.add(update_data.id)
        sql_data_list = db.query(sql_model).filter(sql_model.id.in_({i.id for i in update_list})).all()
        if len(sql_data_list) != len(update_data_id_set):
            raise self.exc(status_code=486, message=f"id: one or many of {update_data_id_set} is not exist",
                           message_code=4)
        for sql_data in sql_data_list:
            update_data = update_data_dict[getattr(sql_data, "id")]
            for item in update_data:
                if item[1] is not None and item[0] != "id":
                    if type(item[1]) is str or type(item[1]) is int:
                        if item[1] in self.null_set:
                            setattr(sql_data, item[0], None)
                        else:
                            setattr(sql_data, item[0], item[1])
                    else:
                        setattr(sql_data, item[0], item[1])
            db.flush()
            db.refresh(sql_data)
        return sql_data_list

    @exception_handler
    def delete_multiple_sql_data(self, db: Session, id_set: set, sql_model):
        stmt = delete(sql_model).where(sql_model.id.in_(id_set))
        db.execute(stmt)
        db.flush()


if __name__ == "__main__":
    pass
