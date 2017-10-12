#!/usr/bin/env python3

import psycopg2

DBNAME = "news"


def get_list_of_popular_articles():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT title, count(*) AS total_views \
              FROM articles, log \
              WHERE slug = substr(path, 10) \
              GROUP BY title \
              ORDER BY total_views DESC \
              LIMIT 3")
    return c.fetchall()
    db.close()


def get_list_of_popular_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT name, count(*) AS total_views \
             FROM authors, articles, log \
             WHERE slug = substr(path, 10) AND authors.id = articles.author \
             GROUP BY name \
             ORDER BY total_views DESC")
    return c.fetchall()
    db.close()


def sum_case():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    c.execute("SELECT to_char(time, 'YYYY-MM-DD') as day_of_month, \
              SUM(CASE WHEN status NOT LIKE '2%' THEN 1 ELSE 0 END) as errors,\
              COUNT(*) as total_hits, \
              (SUM(CASE WHEN status NOT LIKE '2%' THEN 1 ELSE 0 END) / \
              COUNT(*) * 100) AS percentage \
              FROM log \
              GROUP BY day_of_month \
              ORDER BY percentage DESC \
              LIMIT 10;")

    return c.fetchall()
    db.close()


def display_results_of_views(results):
        for each in results:
            print("* %s --- %s views" % each)
        print("\n")


def display_results_of_errors(results):
        for each in results:
            print("* %s --- %s views" % each)
        print("\n")


def main():
    print("What are the most popular three articles of all time?")
    display_results_of_views(get_list_of_popular_articles())

    print("Who are the most popular article authors of all time?")
    display_results_of_views(get_list_of_popular_authors())

    print("On which days did more than 1%% of requests lead to errors?")
    display_results_of_errors(sum_case())


main()
