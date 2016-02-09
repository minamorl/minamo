import redis
from redisorm.core import Persistent
from .models import Page, URL


def _bi(name):
    prefix = "minamo:bi:"
    return prefix + name

def ngram(s, n):
    i = 0
    while True:
        yield s[i:i+n]
        i += 1

        if len(s) <= i:
            return


def create_bigram(page):
    p = Persistent("minamo")
    r = redis.StrictRedis(decode_responses=True)

    if page.description is not None:
        for word in ngram(page.description, 2):
            r.lpush(_bi(word), page.id)
