from . import bot
from . import models
from . import ngram
from redisorm.core import Persistent
from redis import StrictRedis


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


if __name__ == '__main__':
    import sys
    if sys.argv[1] == "crawl":
        bot.bot(sys.argv[2])
        sys.exit()

    if sys.argv[1] == "bi":
        ngram.create_bigram()
        sys.exit()


    if sys.argv[1] == "s":
        show_search_results(sys.argv[2])
