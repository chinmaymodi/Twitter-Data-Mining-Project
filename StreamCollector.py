import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os
import io
import json
import MySQLdb as sql

db=sql.connect(host='localhost', user='root', passwd='',db='datamining')

q = db.cursor()


# Personal Control Variables
collectjson = True
tl = 2
global counter
counter = 0

# Twitter API secrets
ckey = ""
ckeys = ""
atok = ""
atoks = ""


start_time = time.time()
keywords = ['election',
            'elections2016',
            'elections',
            'election2016',
            '2016Election',
            'politics',
            'republicans',
            'democrat',
            'president',
            'trump',
            'DonaldTrump',
            'Trump2016',
            'DonaldTrumpforPresient',
            'hillary',
            'Hillary2016',
            'HillaryClinton',
            'hillaryclinton2016',
            'SaferThanATrumpRally',
            'FeelTheBern',
            'NeverTrump',
            'ImWithHer',
            'MakeDonaldDrumpfAgain',
            'president2016',
            'USElection',
            'CrookedHillary',
            'USpol',
            'PresidentialElections2016',
            'NeverTrump',
            'USPolitics',
            'Trump'
            ]

class listener(StreamListener):

    def __init__(self, start_time, time_limit=60):

        self.time = start_time
        self.limit = time_limit
        self.tweet_data = []

    def on_data(self, data):

        #print ("Got Data", end='\n')

        while (time.time() - self.time) < (self.limit):

            try:
                #is_json(data)
                global counter
                counter += 1
                line = json.loads(data)

                
                if 'created_at' in line:
                    #print(line['created_at'].encode("utf-8", errors='ignore'))
                    l1 = line['created_at'].encode('UTF-8', 'replace')
                    self.tweet_data.append(line['created_at']+"\n")
                else:
                    l1 = "0"
                if 'id' in line:
                    #print(line['id'])
                    l3 = str(line['id']).encode('UTF-8', 'replace')
                    self.tweet_data.append(str(line['id'])+"\n")
                else:
                    l3 = "0"                    
                if 'text' in line:
                    #print(line['text'].encode("utf-8", errors='ignore'))
                    l4 = line['text'].encode('UTF-8', 'replace')
                    self.tweet_data.append(line['text']+"\n")
                else:
                    l4 = "no data available"
                if 'user' in line:
                    if 'id_str' in line['user']:
                        #print(line['user']['id_str']+"\n")
                        l2 = line['user']['id_str'].encode('UTF-8', 'replace')
                        self.tweet_data.append(line['user']['id_str']+"\n")
                    else:
                        l2 = "0"
                else:
                    l2 = "0"
                

                q.execute("""INSERT IGNORE INTO tweet_data (time_created, userid, tweet_id, tweet_data) values (%s, %s, %s, %s)""", (l1, l2, l3, l4))
                
                #self.tweet_data.append(data)
                #self.tweet_data.append('\n')

                return True

            except BaseException(e):
                print ("Failed on_data, " + str(e), end='\n')
                time.sleep(5)
                pass

        
        saveFile = io.open('sample.txt', 'a', encoding='utf-8')
        saveFile.write(''.join(self.tweet_data))
        saveFile.close()
        db.commit()
        q.close()
        db.close()
        global counter
        print("Count is "+str(counter)+".", end='\n')
        exit(0)

    def on_error(self, status):

        print(status)


auth = OAuthHandler(ckey, ckeys)
auth.set_access_token(atok, atoks)

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError():
    print("False")
  print("True")


if __name__ == "__main__":

    print("Hello, the program will run automatically now.")

    if collectjson is True:
        twitterStream = Stream(auth, listener(start_time, time_limit=tl))
        twitterStream.filter(track=keywords, languages=['en'])

    else:
        
        print("Doing non-collection stuff.")
