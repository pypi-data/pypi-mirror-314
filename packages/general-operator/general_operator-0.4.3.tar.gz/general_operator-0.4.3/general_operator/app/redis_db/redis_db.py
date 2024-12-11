import json

import redis
from redis.cluster import ClusterNode
from redis.cluster import RedisCluster


class RedisDB:
    def __init__(self, redis_config, decode_responses=False):
        self.host = redis_config["host"]
        self.db = redis_config["db"]
        self.username = redis_config["user"]
        self.password = redis_config["password"]
        self.decode_responses = decode_responses
        self.socket_timeout = redis_config.get("socket_timeout", 5)
        self.is_cluster = self.__is_redis_cluster()

    def redis_client(self):
        if self.is_cluster:
            return self.__new_cluster()
        else:
            return self.__new_single()

    def __new_cluster(self):
        nodes = [ClusterNode(s.strip().split(":")[0], s.strip().split(":")[1]) for s in self.host.split(",")]
        return RedisCluster(startup_nodes=nodes,
                            username=self.username,
                            password=self.password,
                            socket_timeout=self.socket_timeout,
                            decode_responses=self.decode_responses)

    def __new_single(self):
        return redis.Redis(host=self.host.strip().split(":")[0],
                           port=self.host.strip().split(":")[1],
                           db=self.db,
                           username=self.username,
                           password=self.password,
                           socket_timeout=self.socket_timeout,
                           decode_responses=self.decode_responses)

    def __is_redis_cluster(self):
        host = self.host.split(",")
        if len(host) > 1:
            return True
        else:
            return False


if __name__ == "__main__":
    r = RedisDB(redis_config={
        "host": "127.0.0.1:6379",
        "db": 6,
        "user": "",
        "password": ""
    })
    rdb = r.redis_client()
    d = rdb.hmget("source_group_by_source_id", ["1", "200", "3"])
    print(d)
    for i in d:
        if i:
            a = json.loads(i)
            print(type(a))
            print(a)

