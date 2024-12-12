import redis as RedisClient
from loguru import logger

from . import utils


class Redis(object):

    # https://redis.readthedocs.io/en/stable/_modules/redis/client.html#Redis
    # https://github.com/redis/redis-py#client-classes-redis-and-strictredis
    # redis-py 3.0 drops support for the legacy Redis client class.
    # StrictRedis has been renamed to Redis and an alias named StrictRedis is provided so that users previously using StrictRedis can continue to run unchanged.
    # redis-py 3.0 之后只有一个 Redis, StrictRedis 是 Redis 的别名
    # 这里修改以下参数: host, port, socket_timeout, socket_connect_timeout, charset
    redis = RedisClient.Redis()

    def __init__(self, arguments=None):
        '''Initiation'''
        if utils.v_true(arguments, str):
            self.redis = RedisClient.from_url(arguments)
        elif utils.v_true(arguments, dict):
            self.redis = RedisClient.Redis(**arguments)
        else:
            pass

    def connect_test(self):
        info = 'Redis连接测试'
        try:
            logger.info(f'{info}......')
            self.redis.ping()
            logger.success(f'{info}[成功]')
            return True
        except Exception as e:
            logger.error(f'{info}[失败]')
            logger.exception(e)
            return False

    def flush(self, all=None):
        info = 'Redis数据清理'
        try:
            logger.info(f'{info}......')
            if all == True:
                self.redis.flushall()
            else:
                self.redis.flushdb()
            logger.success(f'{info}[成功]')
            return True
        except Exception as e:
            logger.error(f'{info}[失败]')
            logger.exception(e)
            return False
