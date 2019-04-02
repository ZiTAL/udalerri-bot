#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import path, exit
from json import load, dump
from random import randint
from hashlib import md5
from urllib.parse import quote_plus
from mastodon import Mastodon
from TwitterAPI import TwitterAPI

url = "https://eu.wikipedia.org/w/index.php?search="

# ariñautik erabili duzen berbak hartun #

udalerri_zerrenda = []
udalerri_zerrenda_file = path[0]+"/udalerriak.json" 

with open(udalerri_zerrenda_file, 'r') as f:
	udalerri_zerrenda = load(f)

udalerri_cached = []
udalerri_cache_file = path[0]+"/udalerriak.cache"

with open(udalerri_cache_file, 'r') as f:
	udalerri_cached = load(f)

herriak = []

# cache-atuta daudenak zerrendatik kendu
for u in udalerri_zerrenda:
    hash = md5()
    hash.update(u.encode('utf-8'))
    hash = hash.hexdigest()
    
    if(hash not in udalerri_cached):
        herriak.append(u)

# aleatoidxue hartun

if len(herriak)==0:
    print("udalerri-bot: Bukatu dira udalerriak :)")
    exit()

r = randint(0, len(herriak))
element = herriak[r]

# url-ie sortu
url = url+quote_plus(element)

status = "Egun on "+element+"!!!\n#udalerribot #zitalbot\n"

print("udalerri-bot:")
print("Udalerria: "+element)
print("status: "+status)

#mastodon
mastodon = Mastodon(
    access_token = path[0]+"/mastodon.credentials",
    api_base_url = 'https://mastodon.eus'
)

m = mastodon.status_post(status+url, None)

# twitter
credentials_file = path[0]+"/twitter.credentials"
with open(credentials_file, 'r') as f:
	credentials = json.load(f)

api = TwitterAPI(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'], credentials['ACCESS_TOKEN_KEY'], credentials['ACCESS_TOKEN_SECRET'])
r = api.request('statuses/update', {'status': status+m.url})

# toka dan berbie cache-n sartu #

hash = md5()
hash.update(element.encode('utf-8'))
hash = hash.hexdigest()

udalerri_cached.append(hash)

with open(udalerri_cache_file, 'w') as outfile:
    dump(udalerri_cached, outfile)

exit()