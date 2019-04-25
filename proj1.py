#!/usr/bin/python2.7

import psycopg2

conn = psycopg2.connect('dbname=news')

c = conn.cursor()
c.execute('select title,views from art_acc_desc limit 3;')

results = c.fetchall()
print '\n\n********************\nReport 1\n********************\n'
print 'Article\n---------'
for row in results:
    print row[0] + ' - ' + str(row[1]) + ' views'

c.execute('''select name,sum(views) as views from authors
            join art_acc_desc on id = author group by name;''')

results = c.fetchall()
print '\n\n********************\nReport 2\n********************\n'
print 'Author\n---------'
for row in results:
    print row[0] + ' - ' + str(row[1]) + ' views'

c.execute('select * from errs_as_percent where err_pc > 1 order by date desc;')

results = c.fetchall()
print '\n\n********************\nReport 3\n********************\n'
print 'Date\n---------'

for row in results:
    print row[0] + ' - ' + str(row[1]) + '% errors\n\n'

conn.close
