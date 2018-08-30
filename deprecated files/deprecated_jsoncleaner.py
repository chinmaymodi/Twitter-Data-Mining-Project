import time
import os
import io
import json

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError():
    print("False")
  print("True")



with open("sample.json") as jsondata:
    #is_json(jsondata)
    for line in jsondata:
      #time.sleep(5)
      #print(line)
      #is_json(line)

      if(len(line) > 5):
        is_json(line)
        line=json.loads(line)
        #print(line)
        print(line['created_at'].encode("utf-8", errors='ignore'))
        print(line['id'])
        print(line['text'].encode("utf-8", errors='ignore'))
        '''
        del line['created_at']
        del line['source']
        del line['id_str']
        del line['truncated']
        del line['in_reply_to_status_id']
        del line['in_reply_to_status_id_str']
        del line['in_reply_to_user_id']
        del line['in_reply_to_user_id_str']
        del line['in_reply_to_screen_name']
        del line['user']
        del line['geo']
        del line['coordinates']
        del line['place']
        del line['contributors']
        del line['is_quote_status']
        del line['retweet_count']
        del line['favorite_count']
        del line['entities']
        del line['favorited']
        del line['retweeted']
        del line['possibly_sensitive']
        del line['filter_level']
        del line['lang']
        del line['timestamp_ms']
        '''


print("Test", end='\n')
