from . import bot
from . import models
from redisorm.core import Persistent


def show_search_results(query):
    print("""
Search Result:  {keyword}
==================================================

""".format(keyword=query))

    p = Persistent("minamo")

    for page in p.load_all(models.Page):
        if page.title is None:
            continue

        if query in page.title:
            print("*", page.title)
            print(" ", page.url)


if __name__ == '__main__':
    import sys
    if sys.argv[1] == "crawl":
        bot.bot(sys.argv[2])
        sys.exit()


    if sys.argv[1] == "s":
        show_search_results(sys.argv[2])
