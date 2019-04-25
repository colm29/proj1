# Project 1
This is a newspaper site's reporting tool built in python 2.7 and run from the command line.  Running this program generates three simple reports based on readers accessing site articles.  The reports are run in sequence.  The following three questions are answered by the respective reports:
#### Q 1
What are the most popular three articles of all time?
#### Q 2
Who are the most popular article authors of all time?
#### Q 3
On which days did more than 1% of requests lead to errors?

## Running the Reporting tool
1. Ensure the _newsdata.sql_ file has been run in the _psql_ environment on the linux virtual machine
* `cd` to the vagrant directory from the command line
* copy _proj1.py_ file to this directory
* run `vagrant up` to run the virtual machine
* run `vagrant ssh`
* `cd /vagrant`
* from here `python proj1.py` to run the program

## Program Design
The program is run in python code that connects to a back end psql database called news using the db-api.  Each report prints the results of a query sent to the database.

## PSQL Views
In the psql database _news_, run the following CREATE VIEW statements to create the views needed for this program:

CREATE VIEW art_acc_desc AS
SELECT title,count(title) as views, author FROM log
JOIN articles ON replace(path,'/article/','') = slug
WHERE status = '200 OK'
GROUP BY title,author ORDER BY count(title) DESC;

CREATE VIEW err_on_day AS
SELECT cast(time AS date) AS date, count(*) AS errs
FROM log
WHERE status LIKE '4%' OR status LIKE '5%'
GROUP BY cast(time as date);

CREATE VIEW ok_on_day AS
SELECT cast(time as date) AS date, count(*) AS oks
FROM log
WHERE status = '200 OK'
GROUP BY cast(time AS date);

CREATE VIEW errs_as_percent AS
SELECT TO_CHAR(ok.date, 'Mon dd, yyyy') AS date,round(
((cast(errs as numeric)/(oks + errs))*100),1) AS err_pc
FROM ok_on_day ok JOIN err_on_day er ON ok.date = er.date;
