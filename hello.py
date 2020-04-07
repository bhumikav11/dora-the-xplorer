import requests
import re
from bs4 import BeautifulSoup
import jsonfinder
from scidownl.scihub import *
import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler,Filters
# sx = 'https://ieeexplore.ieee.org/document/6784636'

def check_url(url):
    if bool(re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)) and 'document' in url and 'ieeexplore.ieee.org' in url:
        return True
    else:
        return False

def start(update,context):
    update.messsage.reply_text("Hey, there!")

def echo(update,context):
    update.message.reply_text("Here is the PDF ready to download")

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





