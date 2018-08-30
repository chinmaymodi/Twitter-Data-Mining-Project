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

prot = ['Trump2016', 'DonaldTrumpforPresient', 'CrookedHillary', 'trumppence16', 'maga', 'dncleak', 'neverhillary', 'Donald', 'realDonaldTrump', 'crooked', 'VoteTrump', 'votetrump']
proh = ['Hillary2016', 'hillaryclinton2016', 'NeverTrump', 'ImWithHer', 'MakeDonaldDrumpfAgain', 'Hillary']
neut = ['France', 'france', 'Nice', 'nice']

correctt = 0
wrongt = 0
accuracy = 0

# 753735536351842304 is the last tweet we manually trained
q.execute('''SELECT * FROM tweet_data''')

for row in q:
    tweet = str(row[3])
    
    words = tokeniss(tweet)
    #print("The tweet is: " + tweet, end='\n')
    #print("The token count is: " + str(len(words)), end='\n')


    # First we find out if >= 60% of tokens have a rating
    ratingcount = 0
    for word in words:
        q2.execute('''SELECT count(*) as count from word_ratings where word="''' + str(word) + '''";''')
        for row1 in q2:
            if (row1[0]) != 0:
                ratingcount += 1
    print("The token count is: " + str(len(words)) + " and " + str(ratingcount) + " are present in db.", end='\n')
    if float(float(ratingcount)*1.66666666) < float(len(words)):
        # print("Cannot tokenize this tweet right now, not enough data.", end='\n')
        # Set tweet candidate and rating to 10000 each and skip
        q2.execute('''UPDATE tweet_data SET candidate = 10000, rating = 10000 WHERE tweet_id = ''' + str(row[2]))
        db.commit()
    else:
        # print("Proceeding to rate this tweet.", end='\n')
        # Find out total rating
        # Assign rating to tweet
        # Initialize words in tweet that are not yet initialized
        rsum = 0.000000000001

        # decide pro trump or pro hillary
        candidate = 0
        hc, dc = 0, 0
        for word in words:
            if word in prot:
                dc += 1
            elif word in proh:
                hc += 1
        if dc < 1 and hc < 1:
            candidate = 0
        elif dc > hc:
            candidate = 2
        else:
            candidate = 1

        skiplist=[]

        for word in words:
            q2.execute('''SELECT count(*) as count from word_ratings where word="''' + str(word) + '''";''')
            row2 = q2.fetchone()
            if int(row2[0]) == 0:
                print("This word is not in table, skip it for now and add to list.", end='\n')
                skiplist.append(word)
                continue
            rating = float(0)
            count = float(0)
            if candidate == 0:
                q2.execute('''SELECT hcount, dcount FROM datamining.word_ratings WHERE word = "''' + str(word) + '''"''')
                row2 = q2.fetchone()
                hc, dc = row2[0], row2[1]
                if hc == 0:
                    hc = 1
                if dc == 0:
                    dc = 1
                if float(float(hc)/float(dc)) > float(5):
                    candidate = 1
                if float(float(hc)/float(dc)) < float(0.2):
                    candidate = 2
                if word in neut:
                    candidate = 0
            if candidate == 0:
                # neutral rating
                q2.execute('''SELECT rating, count FROM datamining.word_ratings WHERE word = "''' + str(word) + '''"''')
                row2 = q2.fetchone()
                rating = float(row2[0])
                count = float(row2[1])
                rsum += float(float(rating)/float(count))
            elif candidate == 1:
                #hillary rating unless rating is messed up compared to actual pos/neg connotations
                q2.execute('''SELECT rating, count, hrating, hcount, hp, hn FROM datamining.word_ratings WHERE word = "''' + str(word) + '''"''')
                row2 = q2.fetchone()
                rating = float(row2[0])
                count = float(row2[1])
                if count < 1:
                    count = float(1.0)
                hrating = float(row2[2])
                hcount = float(row2[3])
                if hcount < 1:
                    hcount = float(1.0)
                hp = float(row2[4])
                hn = float(row2[5])
                if (float(float(rating)/float(count)) > 0.0 and hp > hn) or (float(float(rating)/float(count)) > 0.0 and hp > hn):
                    # Here, pos/neg count falls in line with avg rating, so we take avg rating
                    rsum += float(float(rating)/float(count))
                else:
                    rsum += float(float(hrating)/float(hcount))
            elif candidate == 2:
                #trump rating unless < 0.2
                q2.execute('''SELECT rating, count, drating, dcount, dp, dn FROM datamining.word_ratings WHERE word = "''' + str(word) + '''"''')
                row2 = q2.fetchone()
                rating = float(row2[0])
                count = float(row2[1])
                if count < 1:
                    count = float(1.0)
                drating = float(row2[2])
                dcount = float(row2[3])
                if dcount < 1:
                    dcount = float(1.0)
                dp = float(row2[4])
                dn = float(row2[5])
                if (float(float(rating)/float(count)) > 0.0 and dp >= dn) or (float(float(rating)/float(count)) > 0.0 and dp > dn):
                    # Here, pos/neg count falls in line with avg rating, so we take avg rating
                    rsum += float(float(rating)/float(count))
                else:
                    rsum += float(float(drating)/float(dcount))
        print("Tweet is: " + str(tweet), end='\n')
        print("Current sum is " + str(rsum) + " for candidate " + str(candidate), end='\n')
        print("Enter 1 if correct, 2 if wrong, 3 if partially correct: ")
        ans = int(input())
        if ans == 1:
            correctt += 1
        elif ans == 2:
            wrongt += 1
        elif ans == 3:
            correctt += 0.5
            wrongt += 0.5
        print("So far, accuracy is: " + str(float(float(correctt)/float(correctt+wrongt))) + " for " + str(correctt + wrongt) + " values.", end='\n')
        # then assign the +ve or -ve rating to words in skiplist
        for word in skiplist:
            wordrate = 0
            if rsum > 0.2:
                wordrate = 1
            elif rsum < -0.2:
                wordrate = -1
            print("Now we rate " + word + " with rating = " + str(wordrate) + ", count = 1", end='\n')
            if candidate != 0:
                print("Word is for candidate: " + str(candidate), end='\n')
            hcount, hrating, hp, hn, dcount, drating, dp, dn = 0, 0, 0, 0, 0, 0, 0, 0
            if candidate == 1:
                hcount = 1
                if wordrate == -1:
                    hrating = -1
                    hn = 1
                elif wordrate == 1:
                    hrating = 1
                    hp = 1
            elif candidate == 2:
                dcount = 1
                if wordrate == -1:
                    drating = -1
                    dn = 1
                elif wordrate == 1:
                    drating = 1
                    dp = 1
            q3.execute('''INSERT INTO word_ratings (word, rating, count, hcount, hrating, hp, hn, dcount, drating, dp, dn) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (word, str(wordrate), str(count), str(hcount), str(hrating), str(hp), str(hn), str(dcount), str(drating), str(dp), str(dn)))
            db.commit()













