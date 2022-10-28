import pandas as pd
from datetime import datetime
import requests
import json
from dotenv import load_dotenv
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# load .env
load_dotenv()
bot_token = os.environ.get('SLACK_BOT_TOKEN')
app_token = os.environ.get('SLACK_APP_TOKEN')

df = pd.read_excel('src/results/menu_list.xlsx', engine='openpyxl')
today = datetime.now().strftime('%m월 %d일')
todayKoreanMeal = today + '의 *한식*\n' + df.at[0, today] + '\n'
todayCourse = today + '의 *일품*\n' + df.at[1, today]

# slack 함수 사용 위한 작업.
app = App(token = bot_token)

if today in df.columns:
    @app.message("한식") #
    def sendToSay(message, say):
        say(todayKoreanMeal)

    @app.message("일품") #
    def sendToSay(message, say):
        say(todayCourse)

def send_message(token, channel, text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }
    payload = {
        'channel': channel,
        'text': text
    }
    r = requests.post('https://slack.com/api/chat.postMessage',
                      headers=headers,
                      data=json.dumps(payload)
                      )

if __name__ == '__main__':
    if today in df.columns:
        send_message(bot_token, 'C04857SGN2V', todayKoreanMeal + todayCourse)
    else:
        send_message('C04857SGN2V', '오늘의 메뉴가 등록되지 않았습니다. 메뉴 추가를 요청해주세요.')
    SocketModeHandler(app, app_token).start()
