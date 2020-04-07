import requests
import re
from bs4 import BeautifulSoup
import jsonfinder
from scidownl.scihub import *
import os
import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
def check_url(url):
    if bool(re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)) and 'document' in url and 'ieeexplore.ieee.org' in url:
        return True
    else:
        return False

def start(bot, update):
    update.effective_message.reply_text("Dora The Xplorer!")

@run_async
def echo(bot, update):
    if(check_url(update.effective_message.text)):
        data = requests.get(update.effective_message.text)
        soup = BeautifulSoup(data.content, 'html.parser')

        for script in soup.find_all('script'):
            try:
                if 'global.document.metadata' in script.contents[0].string:
                    dat = dict(jsonfinder.only_json(script.contents[0].string)[2])
                    # bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                    update.effective_message.reply_text(dat['title'])
                    if len(dat['abstract']) == 0:
                        update.effective_message.reply_text('There is no abtract for this particular paper.')
                    else:
                        update.effective_message.reply_text(dat['abstract'])
                        update.effective_message.reply_text(dat['doi'])
                    sci = SciHub(dat['doi'], out='output').download(choose_scihub_url_index=0)
                    bot.send_message(chat_id=update.effective_message.chat_id, text=dat['doi'])
                    bot.send_document(chat_id=update.effective_message.chat_id, document=open('output/'+dat['title']+'.pdf', 'rb'))
            except Exception as e:
                print(e)
                pass
    else:
        update.effective_message.reply_text("Not a Valid URL")
    #update.effective_message.reply_text(update.effective_message.text)

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = "1208597229:AAH1Ps2N47ILkz95NoIsn9TPT21iFVNUbPM"
    NAME = "dora-the-xplorer"
    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # Add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()
