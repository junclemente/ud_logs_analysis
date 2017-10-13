# Logs Analysis Project

### Description
This is the Logs Analysis Project for the [Fullstack Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004) at [Udacity.com](https://www.udacity.com "Udacity.com"). In this project, I was provided a PostgreSQL database running in a Vagrant VM. Using Python, I connected to the database using the psycopg2 library to derive answers to three questions. The requirement of the project was to derive the required information with only one query.

### Methods and Issues
There are three tables in the database. Using joins, aggregate functions, and views, I was tasked to answer the following three questions:

1. What are the the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

The first two questions/queries were straightforward with simple inner joins. 

The last question was slightly more challenging. The use of views was allowed but I opted for a different approach: `SUM(CASE WHEN ...)` which seemed to be more efficient, though not covered in the course. I ran into a few issues, but I do not believe these were unique to my approach of using `SUM(CASE WHEN...)`. Using `VIEWS` I also had the same problem. One issues I ran into was that aliases were not acceptable for use in the `WHERE` or `HAVING` clauses. Apparently, `HAVING` and `WHERE` sections are processed prior to the `SELECT` section and therefore I was getting the "alias does not exist" errors. Therefore, the whole function that calculated the percentage had to be rewritten again in the `HAVING` clause. The other issue is that the calculations being performed `PERCENT=(errors/total)*100` resulted in decimals being truncated therefore my calculated results were all `0`. My initial solution was to use `numeric` to ensure that truncation wasn't being performed and that the result had the proper type. This would have allowed for accuracy in the calculation up to a number of decimal places. Since this was not necessary for the project, I opted for a simpler solution: `PERCENT=(errors*100)/total` which eliminated the use of having to deal with decimals numbers. 

### How To Run
To run the application, type `./logsanalysis.py` or `python3 logsanalysis.py` in the same directory

### Languages / Frameworks / Libraries 
* PostgreSQL
* Python3
* psycopg2 
