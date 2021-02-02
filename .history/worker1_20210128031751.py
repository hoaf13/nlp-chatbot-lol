import redis
from typing import Any
import time

red = redis.StrictRedis(host='localhost',
                        port=6379,
                        db=0)