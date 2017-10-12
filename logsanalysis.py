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

# def create_view_errors():
#     db = psycopg2.connect(database=DBNAME)
#     c = db.cursor()
#     c.execute("CREATE VIEW ErrorsLog AS \
#               SELECT to_char(time, 'YYYY-MM-DD') as the_date, COUNT(*) as errors \
#               FROM log \
#               WHERE NOT status LIKE '2%' \
#               GROUP BY the_date;")
#     db.close()
#     print("'ErrorsLog' view created... ")

# def create_view_total_logs():
#     db = psycopg2.connect(database=DBNAME)
#     c = db.cursor()
#     print("Creating view 'TotalLogs'... ")
#     c.execute("CREATE VIEW TotalLogs AS \
#               SELECT to_char(time, 'YYYY-MM-DD') as the_date, \
#               COUNT(*) AS hits \
#               FROM log \
#               GROUP BY the_date;")
#     db.close()
#     print("'TotalLogs' view created...")

# def request_errors():

#     db = psycopg2.connect(database=DBNAME)
#     c = db.cursor()

#     # create_view_errors()
#     print("Creating view 'ErrorsLog'... ")
#     c.execute("CREATE VIEW ErrorsLog AS \
#               SELECT to_char(time, 'YYYY-MM-DD') as the_date, COUNT(*) as errors \
#               FROM log \
#               WHERE NOT status LIKE '2%' \
#               GROUP BY the_date;")
#     print("'ErrorsLog' view created... ")

#     print("Creating view 'TotalLogs'... ")
#     c.execute("CREATE VIEW TotalLogs AS \
#               SELECT to_char(time, 'YYYY-MM-DD') as the_date, \
#               COUNT(*) AS hits \
#               FROM log \
#               GROUP BY the_date;")
#     print("'TotalLogs' view created...")

#     print("Running query...")

#     c.execute("SELECT EL.the_date, \
#               (EL.errors / TL.hits) * 100 AS percentage \
#               FROM ErrorsLog as EL, TotalLogs as TL \
#               WHERE EL.the_date = TL.the_date \
#               GROUP BY EL.the_date, EL.errors, TL.hits \
#               ORDER BY percentage DESC;")
#     print("Query complete...")
#     return c.fetchall()
#     c.execute("DROP VIEW ErrorsLog;")
#     c.execute("DROP VIEW TotalLogs")
#     db.close()

def sum_case():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    c.execute("SELECT to_char(time, 'YYYY-MM-DD') as day_of_month, \
              SUM(CASE WHEN status NOT LIKE '2%' THEN 1 ELSE 0 END) as errors, \
              COUNT(*) as total_hits, \
              (SUM(CASE WHEN status NOT LIKE '2%' THEN 1 ELSE 0 END) / \
              COUNT(*) * 100) AS percentage \
              FROM log \
              GROUP BY day_of_month \
              ORDER BY percentage DESC \
              LIMIT 10;")

    return c.fetchall()
    db.close()

# def total_errors():
#     db = psycopg2.connect(database=DBNAME)
#     c = db.cursor()

#     c.execute("SELECT to_char(time, 'YYYY-MM-DD') AS day_of_month, \
#               COUNT(*) AS errors \
#               FROM log \
#               WHERE status NOT LIKE '2%' \
#               GROUP BY day_of_month \
#               ORDER BY day_of_month;")

#     return c.fetchall()
#     db.close()

# def total_hits():
#     db = psycopg2.connect(database=DBNAME)
#     c = db.cursor()

#     c.execute("SELECT to_char(time, 'YYYY-MM-DD') AS day_of_month, \
#               COUNT(*) AS errors \
#               FROM log \
#               GROUP BY day_of_month \
#               ORDER BY day_of_month;")

#     return c.fetchall()
#     db.close()

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
    display_results(popular_articles())

    print("Who are the most popular article authors of all time?")
    display_results_of_views(get_list_of_popular_authors())

    print("On which days did more than 1% of requests lead to errors?")
    # print(request_errors())
    # print(errors_log())
    # results = sum_case()
    # for each in results:
    #     # print("%s \t %s" %each)
    #     print(each)
    # print(len(results))

    # display_results(total_errors())
    # display_results(total_hits())
# questions()
main()
