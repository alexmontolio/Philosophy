"""
Functions responsible for Wikipedia article
requests and interactions
"""
import re

import requests
from bs4 import BeautifulSoup


# Wikipedia article URLs
WIKI_BASE_URL = 'https://en.wikipedia.org/wiki/'
RANDOM_ARTICLE_URL = 'https://en.wikipedia.org/wiki/Special:Random'


def get_initial_article_title():
    """
    Retrieves a random article from Wikipedia and returns
    its title.

    :return: str
    """
    redirect_response = requests.get(RANDOM_ARTICLE_URL, allow_redirects=False)

    if redirect_response.status_code == 302:
        article_url = redirect_response.headers['location']

        article_title = article_url.split('/')[-1]

    return article_title


def log_article(title, article_store):
    """
    Adds an article title to a set for various purposes, depending
    on which set the the title is placed in

    :param title: the title of an article
    :type title: str

    :param article_store: a container for article titles
    :type article_store: set

    :return: None
    """
    article_store.add(title)


def get_article(article_title):
    """
    Retrieves a Wikipedia article via HTTP and returns its
    HTML contents in bytes

    :param article_title: the title of the article to retrieve
    :type article_title: str

    :return: bytes
    """
    article_url = '{}{}'.format(WIKI_BASE_URL, article_title)

    article_response = requests.get(article_url)

    return article_response.content


def log_article_path(article_title, article_path):
    """
    Adds an article to a container for the purposes of tracking
    the path from the initial article to its possible appendage
    onto the article tree

    :param article_title: the title of the article to retrieve
    :type article_title: str

    :param article_path: the article container for path tracking
    :type article_path: list

    :return: None
    """
    article_path.append(article_title)


def determine_if_article_path_exists(article_title, article_cache, dead_ends):
    """
    Looks thru containers hold articles that have been visited
    and articles which lead to dead end paths to determine if
    a path has already been calculated for the article

    :param article_title: the title of the article to retrieve
    :type article_title: str

    :param article_cache: a container of articles for which a
    path may lead to Philosophy
    :type article_cache: set

    :param dead_ends: a container of articles whose paths will
    not lead to Philosophy
    :type dead_ends: set

    :return: bool
    """
    does_path_exist = False

    if article_title in article_cache or article_title in dead_ends:
        does_path_exist = True

    return does_path_exist


def add_path_to_tree(tree, article_path, article_title, article_cache, dead_ends):
    """
    Adds a given path of articles to the article tree. If an article
    path has no connection to any article node on the tree, the
    articles in the path are removed from the article cache and added
    to a container for articles confirmed to be dead ends.

    Once the appropriate action has been taken, the article path
    container is wiped to make way for the next article path.

    :param tree: the tree containing article paths
    leading to Philosopy
    :type tree: Node

    :param article_path: the article container for path tracking
    :type article_path: list

    :param article_title: the title of the article to retrieve
    :type article_title: str

    :param article_cache: a container of articles for which a
    path may lead to Philosophy
    :type article_cache: set

    :param dead_ends: a container of articles whose paths will
    not lead to Philosophy
    :type dead_ends: set

    :return: None
    """
    if article_title in article_path or article_title in dead_ends:
        article_cache.difference_update(article_path)
        dead_ends.update(article_path)
    else:
        node = tree.find(article_title)

        # Since we are working our way up to the Philosophy article
        # in our tree, we need to reverse the list in order to
        # avoid insert() operations on the article path list
        node.create_path(reversed(article_path))

    del article_path[:]


def get_next_article_title(article):
    """
    Parses a Wikipedia article for the first non-italicized,
    non-parenthesized link and return the title of the
    link's article

    :param article: the HTML contents of a Wikipedia article
    :type article: bytes

    :return: str
    """
    paragraphs = parse_article_paragraphs(article)

    for paragraph in paragraphs:
        a_tag = paragraph.find('a')

        if not a_tag:
            continue

        remove_out_of_scope_tags(paragraph)

        paragraph_ = remove_parenthesize_text_from_paragraph(paragraph)

        try:
            article_path = paragraph_.find('a')['href']
        except TypeError:
            continue

        if article_path:
            article_title = article_path.split('/')[-1]

            return article_title


def parse_article_paragraphs(article):
    """
    Grabs the all paragraph tags under the main article
    section of a Wikipedia article

    :param article: the HTML contents of a Wikipedia article
    :type article: bytes

    :return: str
    """
    soup = BeautifulSoup(article, 'lxml')

    paragraphs = soup.select('.mw-parser-output > p')

    return paragraphs


def remove_out_of_scope_tags(paragraph):
    """
    Removes tags from the article paragraph which are
    out of the scope of the Wikipedia game

    :param paragraph: a Wikipedia article paragraph
    :type paragraph: bs4.BeautifulSoup

    :return: None
    """
    # The test parameters state that only italics need
    # to be removed. But upon investigation, it became
    # clear that a Wikipedia article can have other links
    # that do not link to an article, like anchor links
    # and 'HELP:' links. These links appear to be outside
    # the scope of the assignment, and they even lie outside
    # of the scope of the game as listed in the Wikipedia
    # article which describes this very behavior.
    #
    # Also, the Philosophy game article popped up as a
    # random article during testing. So naturally I had
    # to read it.
    for tag in paragraph.find_all(['small', 'sup', 'i', 'span']):
        tag.replace_with('')


def remove_parenthesize_text_from_paragraph(paragraph):
    """
    Remove text within parentheses from a paragraph

    :param paragraph: a Wikipedia article paragraph
    :type paragraph: str

    :return: bs4.BeatifulSoup
    """
    paragraph_ = str(paragraph)

    paragraph_ = re.sub(r' \(.*?\)', '', paragraph_)

    paragraph_ = BeautifulSoup(paragraph_, 'lxml')

    return paragraph_
