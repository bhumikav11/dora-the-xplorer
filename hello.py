import requests
import re
from bs4 import BeautifulSoup
import jsonfinder
from scidownl.scihub import *
import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler,Filters
# sx = 'https://ieeexplore.ieee.org/document/6784636'



search_term = input()

if(check_url(search_term)):
    data = requests.get(search_term)
    soup = BeautifulSoup(data.content, 'html.parser')

    for script in soup.find_all('script'):
        try:
            if 'global.document.metadata' in script.contents[0].string:
                dat = dict(jsonfinder.only_json(script.contents[0].string)[2])
                print(dat['title'])
                if len(dat['abtract']) == 0:
                    print('There is no abtract for this particular paper.')
                else:
                    print(dat['abstract'])
                sci = SciHub(dat['doi'], out='output').download(choose_scihub_url_index=0)
        except Exception as e:
            pass
else:
    print("Not a Valid URL")



    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger()





