import io
import MySQLdb as sql

db=sql.connect(host='localhost', user='root', passwd='',db='datamining')

q = db.cursor()

file = io.open("sample.txt", 'r+', encoding='utf-8')

l1 = file.readline()

while l1 is not "":
    l2 = file.readline()
    if len(l2) < 3:
        l2 = file.readline()
    l3 = file.readline()
    if len(l3) < 3:
        l3 = file.readline()
    l4 = file.readline()
    if len(l4) < 3:
        l4 = file.readline()

    #print(l1)
    #print(l2)
    #print(l3)
    #print(l4)

    l4 = l4.encode('UTF-8', 'replace')
    l3 = l3.encode('UTF-8', 'replace')
    l2 = l2.encode('UTF-8', 'replace')
    l1 = l1.encode('UTF-8', 'replace')

    #print(l1)
    #print(l2)
    #print(l3)
    #print(l4)

    q.execute("""INSERT IGNORE INTO tweet_data (time_created, userid, tweet_id, tweet_data) values (%s, %s, %s, %s)""", (l1, l2, l3, l4))
    l1 = file.readline()
    if len(l1) < 3:
        l1 = file.readline()
        print("WTF"+'\n')
    
db.commit()
q.close()
db.close()
