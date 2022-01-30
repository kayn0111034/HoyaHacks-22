import logging
import os
import re



from dotenv import load_dotenv
import pyjokes
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

app = App(token=SLACK_BOT_TOKEN, name="Joke Bot")



@app.message("^joke?")
def show_random_joke(message, say):
    #send a random pyjoke back
    
    
    talk_channel = message["channel"]
    user_id = message["user"] 

    joke = pyjokes.get_joke()

    say(text=joke, channel=talk_channel )

@app.action("user_select")
def select_user(ack, action, respond):
    ack()
    respond(f"You selected <@{action['selected_user']}>")

@app.message(re.compile("^knock knock$"))
def ask_who(message, say):
    say("_Who's there?_")



@app.message(re.compile("hello"))
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.message(re.compile("^get help$"))
def ask_who(message, say):
    say(text = "*Help Commands* \n - Office Hours `get office hours` returns the professor/TA's office hours\n - Remind Me `remind me` prompts you to set a reminder for a certain date- \n - Todo List \n - Joke  typing `joke` returns a randomly generated joke")

@app.message(re.compile("^remind me$"))
def show_datepicker(event, say):
    blocks = [{
          "type": "section",
          "text": {"type": "mrkdwn", "text": "Pick a date for me to remind you"},
          "accessory": {
              "type": "datepicker",
              "action_id": "datepicker_remind",
              "initial_date": "2022-01-30",
              "placeholder": {"type": "plain_text", "text": "Select a date"}
          }
        }]
    say(blocks=blocks, text="Pick a date for me to remind you")

@app.message(re.compile("^we will win$"))
def cat(event, say):
    blocks = [
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/challenge_thumbnails/000/911/397/datas/original.png",
                    "alt_text": "HoyaHacks"
                },
                {
                    "type": "mrkdwn",
                    "text": "*HoyaHacks* has approved this message."
                }
            ]
        }
    ]
    say(blocks=blocks, text="Pick a date for me to remind you")

@app.event(("app_mention"))
def event_test(say):
    say("why are you running") 

@app.message(re.compile('^get office hours$'))
def bat(event, say):
    blocks= [
        {
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": "office hours",
                
            },
            "image_url": "https://cdn.discordapp.com/attachments/936637003863302167/937168782126895124/unknown.png",
            "alt_text": "office hours"
        }
    ]
    say(blocks=blocks, text="Pick a date for me to remind you")


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

if __name__=="__main__":
    main()