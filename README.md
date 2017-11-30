# Udacity---Logs-Analysis

by Heber Gonzalez

Project for the Udacity Full Stack Web Developer Nanodegree Program

## Description and Function
This python program is a reporting tool that summerizes data from an SQL database. It doesn't take any input from the user. Instead, it connects to that database, uses SQL queries to analyze the log data, and prints out the answers to some questions.

## Required Libraries and Dependencies
* Psycopg2
* Python3
* Vagrant
* VirtualBox
* PostgreSQL

## Project contents
* README.md
* logs_analysis.py
* logs_analysis_output.txt

## How to Run
1. Install VirtualBox and Vagrant.
2. Download [newsdata.zip](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and unzip it.
3. Put newsdata.sql into the vagrant directory.
4. Then, cd into the vagrant directory and use the command psql -d news -f newsdata.sql.
5. Connect to the 'news' database.
6. Create the views provided in this document.
7. Then run logs_analysis.py in the same directory where the 'news' database is located.

## Views Created
These were the views created within the database.
```SQL
CREATE VIEW popular_articles AS
  SELECT articles.author, title, count(*) as views
  FROM articles, log
  WHERE path = concat('/article/',slug)
  GROUP BY author, title
  ORDER BY views DESC
  LIMIT 8;
```
```SQL
CREATE VIEW status_all AS
  SELECT date(time), status
  FROM log;
```
```SQL
CREATE VIEW status_error AS
  SELECT date, count(*) as status_error
  FROM status_all
  WHERE status = '404 NOT FOUND'
  GROUP BY date
  ORDER BY date;
```
```SQL
CREATE VIEW status_complete AS
  SELECT date, count(*) AS total
  FROM status_all
  GROUP BY date
  ORDER BY date;
```
