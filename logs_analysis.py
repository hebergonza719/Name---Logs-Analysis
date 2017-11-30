#!/usr/bin/env python3

import psycopg2

db_name = 'news'

'''
These were the views created in the database

CREATE VIEW popular_articles AS
SELECT articles.author, title, count(*) as views
FROM articles, log
WHERE path = concat('/article/',slug)
GROUP BY author, title
ORDER BY views DESC
LIMIT 8;
		
CREATE VIEW status_all AS
SELECT date(time), status
FROM log;

CREATE VIEW status_error AS
SELECT date, count(*) as status_error 
FROM status_all
WHERE status = '404 NOT FOUND'
GROUP BY date
ORDER BY date;

CREATE VIEW status_complete AS
SELECT date, count(*) AS total
FROM status_all
GROUP BY date
ORDER BY date;
'''

query_1 = """SELECT title, count(*) AS views
    	FROM articles, log
    	WHERE path = concat('/article/',slug)
    	GROUP BY title
    	ORDER BY views DESC
    	LIMIT 3;
    	"""

query_2 = """SELECT authors.name, 
	sum(popular_articles.views) AS views
	FROM authors, popular_articles
	WHERE authors.id = popular_articles.author
	GROUP BY authors.name
	ORDER BY views DESC;
	"""

query_3 = """SELECT status_error.date, 
	to_char(status_error * 100.0 / total, 'FM999.00') AS percentage
	FROM status_error, status_complete
	WHERE status_error.date = status_complete.date
	AND (status_error * 100.0 / total) > 1.0
	ORDER by date;
	"""

def get_query(query):
	conn = psycopg2.connect(dbname = db_name)
	cursor = conn.cursor()
	cursor.execute(query)
	results = cursor.fetchall()
	conn.close()
	return results

def first_query(query_result):
	print("\n1. What are the most popular three articles of all time?\n")
	for query in query_result:
		print('"{}" --- {} views'.format(query[0], str(query[1])))

def second_query(query_result):
	print("\n2. Who are the most popular article authors of all time?\n")
	for query in query_result:
		print("{} --- {} views".format(query[0], str(query[1])))

def third_query(query_result):
	print("\n3. On which days did more than 1% of requests lead to errors?\n")
	for query in query_result:
		print("{} --- {}% errors".format(query[0], str(query[1])))


first_query(get_query(query_1))
second_query(get_query(query_2))
third_query(get_query(query_3))
