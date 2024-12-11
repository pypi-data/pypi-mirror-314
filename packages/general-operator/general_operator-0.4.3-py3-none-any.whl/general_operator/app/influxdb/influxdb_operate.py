import functools
import influxdb_client
from influxdb_client.client.write_api import WriteOptions
from influxdb_client.rest import ApiException
from urllib3.exceptions import NewConnectionError

from .influxdb import InfluxDB



class InfluxOperate:
    def __init__(self, influxdb: InfluxDB, exc):
        self.influxdb = influxdb
        self.exc = exc
        self.__bucket = influxdb.bucket
        self.__org = influxdb.org
        self.writer = self.influxdb.client.write_api(
            write_options=WriteOptions(
                batch_size=1000,
                flush_interval=10_000,
                jitter_interval=2_000,
                retry_interval=5_000,
                max_retries=5,
                max_retry_delay=30_000,
                max_close_wait=300_000,
                exponential_base=2))
        self.reader = self.influxdb.client.query_api()


    @staticmethod
    def exception_handler(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except NewConnectionError:
                raise self.exc(status_code=488, message="InfluxDB connection failed", message_code=1)
            except ApiException as e:
                raise self.exc(status_code=488, message=str(e.message).replace("\n", ""), message_code=e.status)
            except Exception as e:
                raise self.exc(status_code=488, message='Unknown error', message_code=99)
        return wrapper

    def change_bucket(self, bucket: str):
        self.__bucket = bucket

    def change_org(self, org: str):
        self.__org = org

    def show_bucket(self):
        return self.__bucket

    def show_org(self):
        return self.__org

    @exception_handler
    def write(self, p: influxdb_client.Point | list[influxdb_client.Point]):
        # ex:
        # p = influxdb_client.Point(
        #     "object_value").tag("id", str(_id)) \
        #     .tag("uid", str(uid)) \
        #     .field("value", str(value))
        self.writer.write(bucket=self.__bucket, org=self.__org, record=p)

    @exception_handler
    def query(self, q: str):
        # ex:
        # query = f'''from(bucket:"node_object")
        # |> range(start: {start}, stop: {end})
        # |> filter(fn:(r) => r._measurement == "object_value")
        # |> filter(fn:(r) => r.id == "{_id}")
        # |> filter(fn:(r) => r._field == "value")'''
        data = self.reader.query(org=self.__org, query=q)
        return data
