from redis.client import Redis
from redis.connection import ConnectionPool


class XHMRedis(Redis):
    @classmethod
    def get_db(cls):
        return 0

    @classmethod
    def get_decode_responses(cls):
        return True

    @classmethod
    def get_pool(cls):
        return ConnectionPool(
            host="0.0.0.0",
            port=6379,
            password="",
            db=cls.get_db(),
            encoding="utf-8",
            decode_responses=cls.get_decode_responses(),
        )

    def __init__(self, connection_pool=None):
        connection_pool = connection_pool if connection_pool else self.get_pool()
        super().__init__(connection_pool=connection_pool)
