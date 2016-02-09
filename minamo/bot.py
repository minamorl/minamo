from redisorm.core import Persistent
from .models import Page, URL
import requests
import bs4
import urllib


visited = []
p = Persistent("minamo")
def bot(url, depth=0):
    if is_visited(url) or depth > 3:
        return
    if not url.startswith("http://") and not url.startswith("https://"):
        return
    html = requests.get(url).content
    title = get_title(html)
    links = [join_url(url, x) for x in get_links(html)]
    description = make_description(html)
    page = Page(url=url, title=title, description=description)
    p.save(page)

    print("visiting: ",title, url)
    visit(url)
    for link in links:
        bot(link, depth=depth+1)

# Will be replaced with redis
def is_visited(url):
    global visited
    if url in visited:
        return True
    return False

def visit(url):
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
    
    
