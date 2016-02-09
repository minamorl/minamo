from redisorm.core import Persistent
from .models import Page, URL
from .ngram import create_bigram
import bs4
import urllib
import aiohttp
import asyncio


visited = []
p = Persistent("minamo")


async def bot(session, url):
    links = await request(session, url)

    async with asyncio.Semaphore(5):
        await asyncio.wait([request(session, link) for link in links])


async def request(session, url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return

    async with session.get(url) as response:
        if is_visited(url):
            return
        html = await response.text()
        title = get_title(html)
        print("visiting: ", title, url)
        links = [join_url(url, x) for x in get_links(html)]
        description = make_description(html)
        page = Page(url=url, title=title, description=description)
        p.save(page)
        create_bigram(page)
        mark_as_visited(url)

        return links

# Will be replaced with redis


def is_visited(url):
    global visited
    if url in visited:
        return True
    return False


def mark_as_visited(url):
    global visited
    visited.append(url)


def get_title(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    try:
        title = soup.title.string
    except AttributeError:
        return None
    return title


def get_links(html):
    for link in bs4.BeautifulSoup(html, "html.parser", parse_only=bs4.SoupStrainer('a')):
        if link.has_attr('href'):
            yield link['href']


def make_description(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    return text


def join_url(base, url):
    joinded_url = urllib.parse.urljoin(base, url)
    s, n, path, params, q, frag = urllib.parse.urlparse(joinded_url)[:]
    return urllib.parse.urlunparse((s, n, path, params, None, None))
