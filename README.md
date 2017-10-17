# Logs Analysis Project

### Description
This is the Logs Analysis Project for the [Fullstack Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004) at [Udacity.com](https://www.udacity.com "Udacity.com"). In this project, I was provided a PostgreSQL database running in a Vagrant VM. Using Python, I connected to the database using the psycopg2 library to derive answers to three questions. The requirement of the project was to derive the required information with only one query for each question.

### Methods and Issues
There are three tables in the database. Using joins, aggregate functions, and views, I was tasked to answer the following three questions:

1. What are the the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

The first two questions/queries were straightforward with simple inner joins. 
**UPDATE:** Per recommendation of the first reviewer, I created a subquery to reduce the amount of rows to search in the `log` table. This refactoring reduced the query time by almost 50%. 

The last question was slightly more challenging. The use of views was allowed but I opted for a different approach: `SUM(CASE WHEN ...)` which seemed to be more efficient, though not covered in the course. I ran into a few issues, but I do not believe these were unique to my approach of using `SUM(CASE WHEN...)`. Using `VIEWS` I also had the same problem. One issues I ran into was that aliases were not acceptable for use in the `WHERE` or `HAVING` clauses. Apparently, `HAVING` and `WHERE` sections are processed prior to the `SELECT` section and therefore I was getting the "alias does not exist" errors. Therefore, the whole function that calculated the percentage had to be rewritten again in the `HAVING` clause. The other issue is that the calculations being performed `PERCENT=(errors/total)*100` resulted in decimals being truncated therefore my calculated results were all `0`. My initial solution was to use `numeric` to ensure that truncation wasn't being performed and that the result had the proper type. This would have allowed for accuracy in the calculation up to a number of decimal places. Since this was not necessary for the project, I opted for a simpler solution: `PERCENT=(errors*100)/total` which eliminated the use of having to deal with decimals numbers. **UPDATE:** After the first review, the reviewer recommended that, even though my solution resulted in the correct answer, I should use floats to make my solution more robust. The reviewer also recommended casting `time` as date, ie: `SELECT time::date AS day_of_month` instead of my original solution of `SELECT to_char(time, 'YYYY-MM-DD') AS day_of_month` because the `to_char` function is time consuming. With this change, the query time was significantly reduced. 

Originally, I had three different functions that performed the same thing, with different query statements. This resulted in repetitive functions. The reviewer recommended to create a function that was passed a SQL query statement and also, to add a try/else block to ensure the program fails properly. A new function was created `execute_query(query)` to handle this. 

### Languages / Frameworks / Libraries 
* PostgreSQL v9.5.8
* Python3 v3.5.2
* psycopg2 v2.7.3.1

### How To Run

To use this program, you will need the proper environment with PostgreSQL, Python3 and psycopg2 library installed. A Vagrant Virtual Machine environment can be [forked from Github](https://github.com/udacity/fullstack-nanodegree-vm) if necessary.

Download the database data from here [news database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). Unzip the file and load the data from `newsdata.sql` into the database. This can be done by typing the following into the command line: `psql -d news -f newsdata.sql`. 

Once the database has been setup, you can run the application, by typing `./logsanalysis.py` or `python3 logsanalysis.py`.

