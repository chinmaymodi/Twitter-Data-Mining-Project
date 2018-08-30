import re
import os
import io
import MySQLdb as sql

db = sql.connect(host='localhost', user='root', passwd='', db='datamining')

q = db.cursor()
q2 = db.cursor()

val = 0
count = 0

print("Enter a random number other than 0: ")

val = int(input())

q.execute("""SELECT * FROM tweet_data""")

for row in q:
    count = count + 1
    # print("Type of row5 is " + str(type(row[5])) + " and type of row6 is " + str(type(row[6])), end="\n")
    if row[5] < int(3) and row[5] > int(-3):
        # print("Continuing", end="\n")
        continue
    '''
    print("1")
    print(str(row[0]) + " and type is " + str(type(row[0])))
    print("2")
    print(str(row[1]) + " and type is " + str(type(row[1])))
    print("3")
    print(str(row[2]) + " and type is " + str(type(row[2])))
    print("4")
    print(str(row[3]) + " and type is " + str(type(row[3])))
    print("5")
    print(str(row[4]) + " and type is " + str(type(row[4])))
    print("6")
    print(str(row[5]) + " and type is " + str(type(row[5])))
    print("7")
    print(str(row[6]) + " and type is " + str(type(row[6])))
    '''
    print(str(row[3]))
    #print("\n")
    print("Enter 1 for hillary, 2 for trump, and make it +ve for +ve, -ve for -ve")
    val = int(input())
    print("val is " + str(val))
    print("\n")
    if val == int(-100):
        break
    candidate = 0
    rating = 0
    if val is 1 or val is -1:
        candidate = 1
    elif val is 2 or val is -2:
        candidate = 2
    if val > 0:
        rating = 1
    elif val < 0:
        rating = -1
    querystr = 'UPDATE tweet_data SET rating = ' + str(rating) + ', candidate = ' + str(candidate) + ' WHERE tweet_id="' + str(row[2]) + '"'
    # print(querystr)
    q2.execute(querystr)

print("Ending program, beginning commits", end="\n")
db.commit()
q.close()
db.close()
print("So far you have evaluated " + str(count) + " tweets", end="\n")
if count > 2000:
    print("It's over 2000, you should run the classifier now.", end="\n")
else:
    print("Not enough, you need to train more tweets.", end="\n")
