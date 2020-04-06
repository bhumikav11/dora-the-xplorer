import requests
import re
from bs4 import BeautifulSoup
import jsonfinder
from scidownl.scihub import *
import os
#x = 'https://ieeexplore.ieee.org/document/6784636'

def check_url(url):
    if bool(re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)) and 'document' in url and 'ieeexplore.ieee.org' in url:
        return True
    else:
        return False

search_term = input()

if(check_url(search_term)):
    data = requests.get(search_term)
    soup = BeautifulSoup(data.content, 'html.parser')

    for script in soup.find_all('script'):
        try:
            if 'global.document.metadata' in script.contents[0].string:
                dat = dict(jsonfinder.only_json(script.contents[0].string)[2])
                print(dat['title'])
                print(dat['abstract'])
                sci = SciHub(dat['doi'], out='output').download(choose_scihub_url_index=0)
        except Exception as e:
            pass
else:
    print("Not a Valid URL")