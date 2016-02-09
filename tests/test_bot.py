import urllib.parse
from minamo.models import *
from minamo.bot import *

url = "http://testrun.org/tox/latest/config.html"
title = "tox configuration specification — tox 2.3.1 documentation"
target = Page(url=url, title=title)
html = requests.get(url).content

def test_get_title():
    assert target.title == get_title(html)

def test_get_links():
    print([urllib.parse.urljoin(url, x) for x in get_links(html)])

def test_make_description():
    print(make_description(html))
