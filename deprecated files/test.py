import MySQLdb as sql
import os
import time

db=sql.connect(host='localhost', user='root', passwd='',db='datamining')

query = db.cursor()

query.execute("""SELECT * from tweet_data""")

# row = query.fetchone()
# fetchone() for sequential fetching
# fetchall() to fetch everything

for row in query:
    print(str(row))
    print(row[0])
    row = query.fetchone()
    time.sleep(1)
