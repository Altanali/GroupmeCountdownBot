import os
import json
import datetime
from urllib.parse import urlencode
from urllib.request import  Request, urlopen

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
#target date set
  targetDate = datetime.date(2020, 6, 15)
  currentDate = datetime.date.today()
  # if currentDate < targetDate:
  #     targetDate = targetDate.replace(year=currentDate.year + 1)
  time_to_target = abs(targetDate - currentDate)
  days_to_target = time_to_target.days

  data = request.get_json()

  # We don't want to reply to ourselves!
  msg = ''
#Conditional set to message required for bot to trigger.
  if data['name'] != 'TestBot2' and data['text'] == '!daysleft':
    msg += str(days_to_target) + " days till June 15th, 2020"

    send_message(msg)

  return "ok", 200


def send_message(msg):
    url = 'https://api.groupme.com/v3/bots/post'

    data = {
    #Groupme bot id, saved in Heroku config var
        'bot_id' : os.getenv('GROUPME_BOT_ID'),
        'text' : msg,
        }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read.decode()
