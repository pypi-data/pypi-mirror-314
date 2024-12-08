### redis cache封装

使用:

    from xhm_redis import BoChuRedis
    from redis import ConnectionPool
    
    
    class TranslateRedisCache(BoChuRedis):
        @classmethod
        def get_pool(cls):
            return ConnectionPool(
                host="10.1.251.87",
                port=6379,
                password="",
                db=cls.get_db(),
                encoding="utf-8",
                decode_responses=cls.get_decode_responses()
            )


