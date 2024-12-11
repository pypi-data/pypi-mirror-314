import importlib.util
import os

import redis
from sqlalchemy.orm import Session, sessionmaker

from .General_operate import GeneralOperate
from ..app.influxdb.influxdb import InfluxDB


class AllTableOperator:
    def __init__(self, module, redis_db: redis.Redis, influxdb: InfluxDB, exc):
        self.exc = exc
        self.module = module
        self.redis_db = redis_db
        self.influxdb = influxdb
        self.modules = self.__get_all_modules()
        self.operators = self.__get_all_operator()

    def __get_all_modules(self) -> list:
        imported_modules = []
        path = self.module.__path__[0]
        for filename in os.listdir(path):
            if ((filename.endswith(".py") or filename.endswith(".pyc")) and
                filename != "__init__.py" and filename != "__init__.pyc"):
                # Get the module name by stripping the .py extension
                module_name = ".".join(filename.split(".")[:-1])

                # Construct the module's file path
                module_file_path = os.path.join(path, filename)

                # Load the module dynamically
                spec = importlib.util.spec_from_file_location(module_name, module_file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Add the module to the list
                imported_modules.append(module)

        return imported_modules

    def __get_all_operator(self) -> dict:
        operators = dict()
        for module in self.modules:
            operators[module.__name__] = GeneralOperate(module, self.redis_db, self.influxdb, self.exc)
        return operators

    def initial_all_redis_data(self, db: Session):
        for operator in self.operators.values():
            operator.initial_redis_data(db)
