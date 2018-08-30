import re
import os
import io
import time
import MySQLdb as sql
import nltk
from nltk.tokenize import word_tokenize






keywords = ['election', 'elections2016', 'elections', 'election2016', '2016Election', 'politics', 'republicans', 'democrat', 'president', 'trump', 'DonaldTrump', 'Trump2016',
            'DonaldTrumpforPresient', 'hillary', 'Hillary2016', 'HillaryClinton', 'hillaryclinton2016', 'SaferThanATrumpRally', 'FeelTheBern', 'NeverTrump', 'ImWithHer',
            'MakeDonaldDrumpfAgain', 'president2016', 'USElection', 'CrookedHillary', 'USpol', 'PresidentialElections2016', 'NeverTrump', 'USPolitics', 'Trump']





tweet = """RT @michaelgidley: @alexwhitelive reports on MFB probe after fed election material stored at Melb fire station #springst @MatthewGuyMP http://www.google.com"""
#tweet = """RT @BobRae48: Same "experts" who say #Trump can't win, said #RobFord  and #Brexit wouldn't happen.  All depends on who has momentum in Noveâ¦"""

banlist=['@', ':', 'RT', 'rt', 'rT', 'Rt', '#', '"']
templist=[]


emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def tokeniss(s):
    tokens = preprocess(s)
    for token in tokens:
        if '#' in token or '@' in token or 'â' in token:
            line = re.sub('[#@â]', '', token)
            '''if line not in keywords:
                banlist.append(token)'''
        if 'http' in token or 'www' in token:
            banlist.append(token)

    #print(banlist)

    for token in tokens:
        if token in banlist:
            templist.append(token)
        if len(token) < 4:
            templist.append(token)

    for item in templist:
        if item in tokens:
            tokens.remove(item)

    #print("Final tokens:", end="\n")
    return tokens



    


tokens = preprocess(tweet)
#print(tokens)
#print(str(type(tokens)))

for token in tokens:
    if '#' in token or '@' in token or 'â' in token:
        line = re.sub('[#@â]', '', token)
        '''if line not in keywords:
            banlist.append(token)'''
    if 'http' in token or 'www' in token:
        banlist.append(token)

#print(banlist)

for token in tokens:
    if token in banlist:
        templist.append(token)
    if len(token) < 4:
        templist.append(token)

for item in templist:
    if item in tokens:
        tokens.remove(item)

#print("Final tokens:", end="\n")
#print(tokens)
