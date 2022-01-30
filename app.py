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



@app.message("^get joke?")
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
def ask_help(message, say):
    say(text = "*Help Commands* \n - Office Hours `get office hours` returns the professor/TA's office hours\n - Resources `get resoures` returns online university resources \n - Remind Me `remind me` prompts you to set a reminder for a certain date \n - Joke  typing `get joke` returns a randomly generated joke")

@app.message(re.compile("^get resources$"))
def ask_resource(message, say):
    say(text = "*Resources* \n - Financial Aid `https://uwaterloo.ca/student-awards-financial-aid/` \n - Textbooks `https://open.umn.edu/opentextbooks` \n - Course Advisor `http://catalog.mit.edu/mit/resources/advising-support/`")

@app.message(re.compile("^made by$"))
def made_by(message, say):
    say(text = "*Made By:* \n- Wesley C. \n - Shaun W.\n - McKenna K. \n - Sushrut D. \n - Danny C.")


@app.message(re.compile("^remind me$"))
def remind_me(event, say):
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
def hoya(event, say):
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

@app.message(re.compile('^get office hours$'))
def office_hours(event, say):
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

@app.command("/officy")
def officy(say, ack, body):
    ack("I got it!")
    name = body["text"]
    prof_hours = 'hours not available'
    fpointer = open('office-hours.txt', "r")

    for i in fpointer.readlines():
        line = re.findall(name, i)
        if line:
            prof_hours = i 

    fpointer.close()
    say(text=prof_hours)

@app.event("app_home_opened")
def app_home_opened(event, client, logger):
    user_id = event["user"]

    
        # Call the views.publish method using the WebClient passed to listeners
    result = client.views_publish(
            user_id=user_id,
            view={
                # Home tabs must be enabled in your app configuration page under "App Home"
                # and your app must be subscribed to the app_home_opened event
                "type": "home",
                "blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Welcome to your University Slackspace 🏰",
				"emoji": True
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "image",
					"image_url": "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg",
					"alt_text": "cute cat"
				},
				{
					"type": "mrkdwn",
					"text": "*Cat* has approved this message."
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*University Updates*"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "News",
					"emoji": True
				},
				"value": "News",
				"url": "https://www.georgetown.edu/news/",
				"action_id": "button-action"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Dining Hall/Food Options*"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Menu",
					"emoji": True
				},
				"value": "click_me_123",
				"url": "https://www.hoyaeats.com/menu-hours/",
				"action_id": "button-action"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Report Absence*"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Absence",
					"emoji": True
				},
				"value": "click_me_123",
				"url": "https://google.com",
				"action_id": "button-action"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Weather Forecast*"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Weather",
					"emoji": True
				},
				"value": "click_me_123",
				"url": "https://www.accuweather.com/en/us/georgetown/20007/weather-forecast/2218409",
				"action_id": "button-action"
			}
		},
		{
			"type": "image",
			"image_url": "https://osei.georgetown.edu/wp-content/uploads/sites/258/2020/01/SSH-Georgetown-Campus-scaled.jpg",
			"alt_text": "inspiration"
		},
		{
			"type": "divider"
		}
	],
            },
        )
    logger.info(result)


    

def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

if __name__=="__main__":
    main()