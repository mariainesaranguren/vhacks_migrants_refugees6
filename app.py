  
#Python libraries that we need to import for our bot
import random
import os
from flask import Flask, request, send_file, render_template, send_from_directory
import requests
from pymessenger.bot import Bot
import six
import six.moves.urllib as urllib
from google.cloud import translate
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getcwd()+'/project_keys.json'

#global var to genreate translation text files
num = 1

app = Flask(__name__)
#fb page access and verfify tokens
ACCESS_TOKEN = 'EAACZAvQ2phPMBANalkw6QQnsws921Eeuik8I2N7c7CuutB41T56XAZAiTpzP4AQInVe8x9d345MzZAhFzC1w61sE2ZA3gutLN7S9KXTcXRPYekfNMV4vpM92Y2eJpHssSQZAeE7Cm5R9osG3JZCwD68yIHPEooxiyag5KVSPMs9AZDZD'
VERIFY_TOKEN = 'getLavoroKey'
bot = Bot(ACCESS_TOKEN)
 
#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message our bot, Facebook has implemented a verify token
        that confirms all requests that our bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else: # request is POST
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                m = message.get('message')
                # post was reached
                if not bool(m):
                    p = message.get('postback')
                    if p:
                        m = {'text':p['payload']}
                if m:
                    txt_received = m.get('text')
                    if txt_received:
                        recipient_id = message['sender']['id']
                        if txt_received.lower() == 'a' or txt_received.lower() == 'd':
                            post_to_lavoro(txt_received.lower(), recipient_id), job_id)
                            return "Message Processed"
                    """
                        #translate text
                        #TODO: check if txt is not english
                        transfer_to_translate(txt_received)
                        post_to_lavoro('./translateFiles/vtext{}.txt'.format(num), id_to_phone.get(recipient_id))
                        return "Message Processed"
                    """
                else:
                    return "NOT PROCESSED- no text present"
 
#this function sends a POST request to our backend, letting it know whether user
#wants a job or should have more offers sent 
def post_to_lavoro(signal, fb_UserID, jobPost_id):
    #sending accept/reject of a job offer
    if not jobPost_id or fb_UserID:
        return
        #TODO: change the post address to our database end

    r = requests.post('https://5060ffdc.ngrok.io/bot', json = {'message' : signal})


#this function calls the google translate API to translate a message
def transfer_to_translate(text, target):
    #Translates text into the target language.
    #Target must be an ISO 639-1 language code.
    #See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    
    translate_client = translate.Client()
        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client.translate(
            text, target_language=target)

        # print(u'Text: {}'.format(result['input']))
        # print(u'Translation: {}'.format(result['translatedText']))
        # print(u'Detected source language: {}'.format(
        #     result['detectedSourceLanguage']))

        return result['translatedText']



def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'
 
# listen for lavoro text messages (job descriptions)
@app.route("/lavoro-text", methods=['POST'])
def get_lavoro_text():
    if request.method == 'POST':
        # get input message
        info = request.get_json()
        """
        user_id = info['user_id']
        job_descr = info['job_description']
        """
        send_fb_message(user_id, info)
        return ('', 204)


#chooses a random message to send to the user
def get_message():
    sample_responses = ["Message 1", "message 2", "message 3", "message 4"]
    # return selected item to the user
    return random.choice(sample_responses)
 
#uses PyMessenger to send response to user
def send_fb_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    
    #TODO:
        #"text":response['job_description']
        #send job with accept/decline buttons:
        if response['job_description']:
            if response['langugage'] != 'en':
                #translate first argument into language in second argument
                msg = transfer_to_translate('We found you a new job!', response['langugage'])
                job_desc = transfer_to_translate(response['job_description'], response['language'])
                acceptButt = transfer_to_translate('I want it!', response['langugage'])
                declineButt = transfer_to_translate('Decline the offer', response['langugage'])
            else:
                msg = 'We found you a new job!'
                job_desc = response['job_description']
                acceptButt = 'I want it!'
                declineButt = 'Decline the offer'

        # construct payload and send it
        payload = {
        "recipient":{ "id":recipient_id},
        "message":{
                "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"{} \/n {}".format(msg ,job_desc),
                    "buttons":  [
                                    {
                                    "type":"postback",
                                    "title":acceptButt,
                                    "payload": "a"
                                    },
                                    {
                                    "type":"postback",
                                    "title":declineButt,
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

