import redis
from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker, Session
from fastapi.responses import JSONResponse


from ..dependencies.db_dependencies import create_get_db
from ..function.all_table import AllTableOperator
from ..app.influxdb.influxdb import InfluxDB


class AllTableRouter(AllTableOperator):
    def __init__(self, module, redis_db: redis.Redis, influxdb: InfluxDB, exc,
                 db_session: sessionmaker, is_initial=False, include_in_schema=False):
        self.redis_db = redis_db
        self.influxdb = influxdb
        self.exc = exc
        self.db_session = db_session
        self.is_initial = is_initial
        self.include_in_schema = include_in_schema
        AllTableOperator.__init__(self, module, redis_db, influxdb, exc)

    def create(self):
        router = APIRouter(
            prefix=f"/all_operator",
            tags=[f"All Operator"],
            dependencies=[],
            include_in_schema=self.include_in_schema,
        )
        @router.on_event("startup")
        async def task_startup_event():
            if self.is_initial:
                db = self.db_session()
                AllTableOperator.initial_all_redis_data(self, db)
                db.close()

        @router.get("/reload_table/",)
        async def reload_table(db: Session = Depends(create_get_db(self.db_session))):
            AllTableOperator.initial_all_redis_data(self, db)
            return JSONResponse(content="ok")
        return router

if __name__ == "__main__":
    pass