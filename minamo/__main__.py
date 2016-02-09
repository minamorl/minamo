from . import bot
from . import models
from . import ngram
from redisorm.core import Persistent
from redis import StrictRedis
import asyncio
import aiohttp


def show_search_results(query):
    print("""
Search Result:  {keyword}
==================================================

""".format(keyword=query))

    p = Persistent("minamo")
    r = StrictRedis(decode_responses=True)

    qgram = ngram.ngram(query, 2)

    resultset = None
    for bi in list(qgram)[:-1]:
        if resultset is None:
            resultset = set(r.lrange("minamo:bi:{}".format(bi), 0, -1))
        else:
            resultset = resultset & set(r.lrange("minamo:bi:{}".format(bi), 0, -1))
    print(resultset)

    for page in (p.load(models.Page, x) for x in resultset):
        if page.title is None:
            continue

        print("*", page.title)
        print(" ", page.url)


def main():
    import sys
    import asyncio

    if sys.argv[1] == "crawl":
        loop = asyncio.get_event_loop()
        with aiohttp.ClientSession(loop=loop) as session:
            loop.run_until_complete(bot.bot(session, sys.argv[2]))
        sys.exit()

    if sys.argv[1] == "s":
        show_search_results(sys.argv[2])

if __name__ == '__main__':
    main()
