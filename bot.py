
import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter
import os
import logging
from tinydb import TinyDB, Query
import re

SLACK_TOKEN = os.environ['SLACK_TOKEN']
SIGNING_SECRET = os.environ['SIGNING_SECRET']
 
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)
 
client = slack.WebClient(token=SLACK_TOKEN)
 
# initialize logger
FORMAT = '%(asctime)s %(channel)-15s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT, filename='bot.log', filemode='a',)
logger = logging.getLogger('slack_loggger')

# Initialize DB and tables
db = TinyDB('./db.json')
users_table = db.table('users')
set_up_table = db.table('set_up')
# Create quary object for DB
quary = Query()

set_up_table.upsert({'setup': 'Panther01', 'used_by': 'ella'}, quary.setup == 'Panther01')
print(set_up_table.all())

@ slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
 
    if re.compile(r'bootstrap db.*').match(text):
        try:
            set_up_table.insert_multiple(text.replace('bootstrap db ', ''))
        except Exception as err:
            logger.warning('error with boostrap database: %s',
                            err,
                            extra={'user': user_id, 'channel': channel_id})
            client.chat_postMessage(channel=channel_id,
                                    text=f"something went wrong {err}")
    elif re.compile(r'using.*').match(text):
        try:
            setup = text.replace('using ', '')
            set_up_table.upsert(
                {'setup': setup, 'user': user_id}, quary.setup == setup)
        except Exception as err:
            logger.warning('error with updating used server: %s',
                            err,
                            extra={'user': user_id, 'channel': channel_id})
            client.chat_postMessage(channel=channel_id,
                                    text=f"something went wrong {err}")
    elif re.compile(r'free setup.*').match(text):
        try:
            setup = text.replace('free setup ', '')
            set_up_table.upsert(
                {'setup': setup, 'user': ''}, quary.setup == setup)
        except Exception as err:
            logger.warning('error with updating used server: %s',
                            err,
                            extra={'user': user_id, 'channel': channel_id})
            client.chat_postMessage(channel=channel_id,
                                    text=f"something went wrong {err}")
    elif re.compile(r'show all.*').match(text):
        try:
            client.chat_postMessage(channel=channel_id,
                                    text=str(set_up_table.all()))
        except Exception as err:
            logger.warning('error with updating used server: %s',
                            err,
                            extra={'user': user_id, 'channel': channel_id})
            client.chat_postMessage(channel=channel_id,
                                    text=f"something went wrong {err}")
    else:
        client.chat_postMessage(channel=channel_id,
                                    text=f"help!")
if __name__ == "__main__":
    app.run(debug=True)
