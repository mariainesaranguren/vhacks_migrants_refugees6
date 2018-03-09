  
#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
 
app = Flask(__name__)
ACCESS_TOKEN = 'EAACZAvQ2phPMBANalkw6QQnsws921Eeuik8I2N7c7CuutB41T56XAZAiTpzP4AQInVe8x9d345MzZAhFzC1w61sE2ZA3gutLN7S9KXTcXRPYekfNMV4vpM92Y2eJpHssSQZAeE7Cm5R9osG3JZCwD68yIHPEooxiyag5KVSPMs9AZDZD'
VERIFY_TOKEN = 'getLavoroKey'
bot = Bot(ACCESS_TOKEN)
 
#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_fb_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_fb_message(recipient_id, response_sent_nontext)
    return "Message Processed"
 
 
def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'
 
 
#chooses a random message to send to the user
def get_message():
    sample_responses = ["Message 1", "message 2", "message 3", "message 4"]
    # return selected item to the user
    return random.choice(sample_responses)
 
#uses PyMessenger to send response to user
def send_fb_message(recipient_id, response):
    #sends user the text message provided via input response parameter

    #TODO:
        #if response = 'job found':
            #send job with accept/decline buttons:
        #if response == "To accept type A, to decline type D":
        # construct payload and send it
        payload = {
        "recipient":{ "id":recipient_id},
        "message":{
                "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"We found you a new job!",
                    "buttons":  [
                                    {
                                    "type":"postback",
                                    "title":"I want it!",
                                    "payload": "a"
                                    },
                                    {
                                    "type":"postback",
                                    "title":"Decline the offer",
                                    "payload": "d"
                                    },
                                ]
                }}}}
        r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(ACCESS_TOKEN), json = payload)
        return "success"
    #TODO: #this is commented out because the pervious code is not inside an if statemnt. Once it is, then the if will check
    # if there's a new job and only sent the json with button if there is. otherwiswe we just return something else that is 
    #defined below this line
    #bot.send_text_message(recipient_id, response)
    #return "success"
 
if __name__ == "__main__":
    app.run()

