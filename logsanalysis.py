#!/usr/bin/env python3
import sys
import psycopg2

DBNAME = "news"


def execute_query(query_param):
    """Connects to and queries the database and returns a list of tuples.

    Parameters
    ----------
    query_param: string
        SQL query statement to be executed.

    Returns
    -------
    result:
        List of tuples.

    Raises
    ------
    Exception
        Execution will exit if an error is encountered.
    """

    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute(query_param)
        result = c.fetchall()
        db.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print("*********************************\n"
              "* An error was encountered.     *\n"
              "* This program cannot continue. *\n"
              "*********************************\n"
              "Error Message:")
        sys.exit(error)


def display_results_of_views(results):
    """Displays the results of article views."""
    if len(results) > 0:
        for each in results:
            print("* {0} --- {1} views".format(*each))
        print("\n")
    else:
        print("There were no results that matched the query.")


def display_results_of_errors(results):
    """Displays the results for percentage of errors."""
    if len(results) > 0:
        if (len(results)) == 1:
            print("There was a total of one day: ")
        else:
            print("There were a total of {} days: ".format(len(results)))
        for date, percent in results:
            print("* Date: {d: %Y %B %d} --- {p:.2f}% errors"
                  .format(d=date, p=percent))
    else:
        print("There were no days that had 1 percent or greater "
              "request errors.")


def main():
    """Prints the question and calls function with proper SQL query."""

    print("What are the most popular three articles of all time?")
    """Queries the database to get a list of article titles and the number of
    times they have been viewed and orders the most popular articles at the top
    in descending order.
    """
    query_most_popular_articles = """
        SELECT title, views
        FROM articles
        INNER JOIN (SELECT path, COUNT(path) AS views
                    FROM log
                    GROUP BY path) AS log
        ON log.path = '/article/' || articles.slug
        ORDER BY views DESC
        LIMIT 3;
        """
    results = execute_query(query_most_popular_articles)
    display_results_of_views(results)

    print("Who are the most popular article authors of all time?")
    """Queries the database to return a list of authors and the total number of
    times their articles have been viewed ordered in descending order with the
    most popular author first.
    """
    query_most_popular_authors = """
        SELECT name, sum(views) as total
        FROM authors, articles
        INNER JOIN (SELECT path, COUNT(path) AS views
                    FROM log
                    GROUP BY path) AS log
        ON '/article/' || slug = path
        WHERE authors.id = articles.author
        GROUP BY name
        ORDER BY total DESC;
        """
    results = execute_query(query_most_popular_authors)
    display_results_of_views(results)

    print("On which days did more than 1 percent of requests lead to errors?")
    """Queries the database to calculate the percentage of errors versus the
    total of requests per day.
    """
    query_percent_of_errors = """
        SELECT time::date as day_of_month,
        (SUM(CASE WHEN status NOT LIKE '2%' THEN 1 ELSE 0 END)::numeric
        / COUNT(*) * 100) AS percentage
        FROM log
        GROUP BY day_of_month
        HAVING ((SUM(CASE WHEN status NOT LIKE '2%'
                   THEN 1 ELSE 0 END) * 100)/COUNT(*)) >= 1
        ORDER BY percentage DESC;
        """
    results = execute_query(query_percent_of_errors)
    display_results_of_errors(results)


# Call the main function to begin queries and calculations.
if __name__ == "__main__":
    main()
