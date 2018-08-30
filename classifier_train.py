import os
import io
import time
import MySQLdb as sql
from classifier import tokeniss

db = sql.connect(host='localhost', user='root', passwd='', db='datamining')
q = db.cursor()             # Cursor for getting all tweets
q2 = db.cursor()            # Cursor for getting word count from table
q3 = db.cursor()            # Cursor for updating word count or adding word to table

# row is for returned rows of q
# row2 is for returned values of q2
# row3 is for returned row of q3

'''
#This file basically uses classifier.py in an easy to use format
# Build on this file to contact database and update word scores


tweet="""RT @drJim4Bernie: It's so much fun to watch them squirm. these Judas Goats from @MoveOn (A ClintonFront day 1) BTW
Bernie beats Trump httpsâ¦"""

print(tokeniss(tweet))

'''

starttime = time.time()

q.execute("""SELECT * FROM tweet_data""")

for row in q:
    if int(row[2]) > int(753735536351842304):
        print("Reached end of training data, breaking now.")
        break
    tweet = str(row[3])
    words = tokeniss(tweet)
    #print("Tweet is: " + tweet + ", and word list is: " + str('\n') + str(words))
    for word in words:
        #print(word)
        q2.execute('''SELECT count(*) as count from word_ratings where word="''' + str(word) + '''";''')
        for row1 in q2:
            #print("Row obtained is: " + str(row1), end='\n')
            if int(row1[0]) == 0:
                # add word to table
                #print("Adding " + str(word) + " to table.", end='\n')
                rating = 0
                if int(row[5]) > 0:
                    rating = 1
                elif int(row[5]) < 0:
                    rating = -1
                count = 1
                hcount, hrating, hp, hn, dcount, drating, dp, dn = 0, 0, 0, 0, 0, 0, 0, 0
                if int(row[4]) == -1 or int(row[4]) == 1:
                    hcount = 1
                    if int(row[5]) == int(1):
                        hp = 1
                    elif int(row[5]) == int(-1):
                        hn = 1
                elif int(row[4]) == -2 or int(row[4]) == 2:
                    dcount = 1
                    if int(row[5]) == int(1):
                        dp = 1
                    elif int(row[5]) == int(-1):
                        dn = 1
                q3.execute('''INSERT INTO word_ratings (word, rating, count, hcount, hrating, hp, hn, dcount, drating, dp, dn) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (word, str(rating), str(count), str(hcount), str(hrating), str(hp), str(hn), str(dcount), str(drating), str(dp), str(dn)))
                db.commit()
            else:
                # add to count of word
                #print("Updating count of " + str(word) + ".", end='\n')
                q3.execute('''SELECT * from word_ratings where word="''' + str(word) + '''";''')
                row3=q3.fetchone()
                #q3.close()
                rating, count, hcount, hrating, hp, hn, dcount, drating, dp, dn = int(row3[1]), int(row3[2]), int(row3[3]), int(row3[4]), int(row3[5]), int(row3[6]), int(row3[7]), int(row3[8]), int(row3[9]), int(row3[10])
                if int(row[5]) > 0:
                    rating += 1
                elif int(row[5]) < 0:
                    rating -= 1
                count += 1
                if int(row[4]) == int(1) or int(row[4]) == int(-1):
                    hcount += 1
                    if int(row[5]) == int(1):
                        hp += 1
                    elif int(row[5]) == int(-1):
                        hn += 1
                elif int(row[4]) == int(2) or int(row[4]) == int(-2):
                    dcount += 1
                    if int(row[5]) == int(1):
                        dp += 1
                    elif int(row[5]) == int(-1):
                        dn += 1
                updatestr = '''UPDATE word_ratings SET rating = ''' + str(rating) + ''', count = ''' + str(count) + ''', hcount = ''' + str(hcount) + ''', hrating = ''' + str(hrating) + ''', hp = ''' + str(hp) + ''', hn = ''' + str(hn) + ''', dcount = ''' + str(dcount) + ''', drating = ''' + str(drating) + ''', dp = ''' + str(dp) + ''', dn = ''' + str(dn) + ''' WHERE word = "''' + str(word) + '''"'''
                q3.execute(updatestr)
                db.commit()
    #time.sleep(5)
    #print("Elapsed time is: " + str((time.time()) - starttime) + ".", end='\n')
q.close()
q2.close()
q3.close()
db.commit()
db.close()
endtime = time.time()

print("Total time taken is: " + str(endtime - starttime) + ".", end='\n')
