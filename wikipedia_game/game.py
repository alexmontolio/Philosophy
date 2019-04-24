"""
The Wikipedia Philosophy Game

A strange occurance where articles lead to the
Philosophy article on Wikipedia, implemented
in a non-brute force fashion
"""
import os
import csv
import datetime
from operator import itemgetter

from wikipedia_game.article import *
from wikipedia_game.tree_node import Node


# String 'constant' values
PHILOSOPHY_ARTICLE = 'Philosophy'
OUTPUT_FILE_NAME = 'distance-to-philosophy-{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d%H%M%S')
)
CSV_OUTPUT_MESSAGE = 'Results successfully written to {}'


def get_distance_of_initial_articles(node, articles, results, distance=0):
    """
    Finds the distance of all initial random article

    :param node: the starting node of the article tree
    :type node: Node

    :param articles: a container with the titles of all
    initial articles
    :type articles: set

    :param results: a container to hold the article
    distances from Philosophy
    :type results: list

    :param distance: the initial value to set for the
    distance from the starting node
    :type distance: int

    :return: None
    """
    if node.name in articles:
        results.append((distance, node.name))
        articles.remove(node.name)
        return distance

    if distance is 0 or distance is None:
        distance_ = 0
    else:
        distance_ = distance

    for node_ in node.children:
        distance = get_distance_of_initial_articles(
            node_, articles, results, distance_ +1
        )

    return distance


def format_results_of_game(tree, initial_articles, results):
    """
    Converts the article tree into a list of results
    sorted by an article's distance from the Philosophy
    article.

    :param tree: the tree containing article paths to
    the Philosophy article
    :type tree: Node

    :param initial_articles: a container for the initial
    articles in the game
    :type initial_articles: set

    :param results: a container to hold the article
    distances from Philosophy
    :type results: list

    :return: None
    """
    get_distance_of_initial_articles(
        tree, initial_articles, results, distance=0
    )

    for article in initial_articles:
        results.append((0, article))

    results.sort(key=itemgetter(0))


def output_results_to_csv(results):
    """
    Creates a CSV file containing the result of the
    Philosophy game.

    :param results: a container to hold the article
    distances from Philosophy
    :type results: list

    :return: None
    """
    output_path = os.path.join(os.getcwd(), OUTPUT_FILE_NAME)
    HEADERS = ['Article', 'Distance To Philosophy']

    with open(output_path, 'w') as fp:
        writer = csv.writer(fp, delimiter=',')

        writer.writerow(HEADERS)

        for result in results:
            distance = result[0] or 'No Path'
            print(distance)
            article = result[1]
            writer.writerow([article, distance])

    print(CSV_OUTPUT_MESSAGE.format(output_path))


def calculate_successful_article_percent(article_cache, dead_ends):
    """
    Calculates the percentage of articles which lead to
    the Philosophy article

    :param article_cache: a container of articles for which a
    path may lead to Philosophy
    :type article_cache: set

    :param dead_ends: a container of articles whose paths will
    not lead to Philosophy
    :type dead_ends: set

    :return: float
    """
    if None in dead_ends:
        dead_ends.remove(None)

    article_percentage = 100 - (len(dead_ends)/len(article_cache) * 100)

    return float("{0:.2f}".format(article_percentage))


def main():
    """
    Given Task:

    On Wikipedia, you'll find that by clicking the first
    non-italicized and non-parenthesized link in an article,
    and repeating this process, will very often eventually
    lead to the Philosophy article.

    Use the "Random article" link in the left sidebar of any
    article to randomly select an article to determine how
    many articles you need to go through to get to the
    Philosophy article.
    """
    initial_articles = set()
    dead_ends = set()
    article_cache = {PHILOSOPHY_ARTICLE}
    article_path = []

    tree = Node(PHILOSOPHY_ARTICLE)

    turn = 5

    turn_log_message = 'Starting Turn {}: {}'

    while turn < 11:
        article_title = get_initial_article_title()
        
        if article_title in article_cache:
            continue

        print(turn_log_message.format(turn, article_title))

        log_article(article_title, initial_articles)

        while article_title != PHILOSOPHY_ARTICLE:
            article = get_article(article_title)

            does_path_exist = determine_if_article_path_exists(
                article_title, article_cache, dead_ends
            )

            if does_path_exist:
                break

            log_article(article_title, article_cache)
            log_article_path(article_title, article_path)

            article_title = get_next_article_title(article)

        add_path_to_tree(
            tree, article_path, article_title, article_cache, dead_ends
        )

        turn += 1

    results = []

    format_results_of_game(tree, initial_articles, results)

    output_results_to_csv(results)

    success_rate = calculate_successful_article_percent(
        article_cache, dead_ends
    )

    return success_rate


if __name__ == '__main__':
    success_rate = main()
    print(
        'The average success rate for random articles is {}%.'.format(
            success_rate
        )
    )
