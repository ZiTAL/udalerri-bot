#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys          import path, exit
from json         import load, dump
from random       import randint
from hashlib      import md5
from urllib.parse import quote_plus
from mastodon     import Mastodon

#from time import localtime
#from time import strftime

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

# gudoten bat hartun
"""
local_time = localtime()
local_time = strftime("%m-%d", local_time)

if(local_time=="04-02"):
    element = "Barrika"
else:
    r = randint(0, len(herriak))
    element = herriak[r]
"""

r = randint(0, len(herriak))
element = herriak[r]

# url-ie sortu
url = url+quote_plus(element)

status = "Egun on "+element+"!!!\n#udalerribot #zitalbot\n"

print("udalerri-bot:")
print("Udalerria: "+element)
print("status: "+status)

#mastodon

with open(path[0]+"/mastodon.json", 'r') as f:
   mastodon_config = load(f)

mastodon = Mastodon(
   access_token = mastodon_config['token'],
   api_base_url = mastodon_config['instance']
)

m = mastodon.status_post(status=status+url, visibility="public")

# toka dan berbie cache-n sartu #

hash = md5()
hash.update(element.encode('utf-8'))
hash = hash.hexdigest()

udalerri_cached.append(hash)

with open(udalerri_cache_file, 'w') as outfile:
    dump(udalerri_cached, outfile)

exit()