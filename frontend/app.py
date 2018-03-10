#Python libraries that we need to import for our bot
import random
import os
from flask import Flask, jsonify, request, send_file, render_template, send_from_directory, session, redirect, url_for 
import requests
from pymessenger.bot import Bot
from google.cloud import translate
import six
import six.moves.urllib as urllib


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getcwd()+'/project_keys.json'

#global var to genreate translation text files
num = 1
app = Flask(__name__)
app.secret_key = os.urandom(24)
#fb page access and verfify tokens
ACCESS_TOKEN = 'EAACZAvQ2phPMBAPwEXUYHXgfxBZBpPLZAJo7Q14OdfaD2yvZBY3xBMISlSAkEt82gzb6Hi0xTwKSKBH7T5qJ2dXDEr0dQ9JsCsLtjEKCWq70aZB01ZAGyjs5T6jdJ7jGNfwMAm1oIpohzWb3ZBA7tKysPaJZBaPaR0ZCzQDyCVReOSAZDZD'
VERIFY_TOKEN = 'getLavoroKey'
bot = Bot(ACCESS_TOKEN)

#################################################
#website handling:
###################################################
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login_it")
def login_it():
	session['language'] = 'IT'
	return render_template("login.html")

@app.route("/login_gb")
def login_gb():
	session['language'] = 'EN'
	return render_template("login.html")

@app.route("/login_sy")
def login_sy():
	session['language'] = 'AR'
	return render_template("login.html")

@app.route("/login_es")
def login_es():
	session['language'] = 'ES'
	return render_template("login.html")

@app.route("/login_post", methods=["POST"])
def login_post():
	session['user_id'] = request.json
	return '{}'

@app.route("/role")
def role():
	return render_template("role.html")

@app.route("/poster_info")
def poster_info():
	return render_template("user_info.html", jobs=True)

@app.route("/skills_want", methods=["GET", "POST"])
def skills_want():
	if request.method == 'GET':
		return render_template("skills.html", title="Select Skills You Want")
	else:
		skills = request.form.getlist('skill')
		session['skills'] = skills
		return redirect(url_for('poster_info'))

@app.route("/skills", methods=["GET", "POST"])
def skills():
	if request.method == 'GET':
		return render_template("skills.html", title="Select Skills You Have")
	else:
		skills = request.form.getlist('skill')
		session['skills'] = skills
		return redirect(url_for('user_info'))

@app.route("/user_info")
def user_info():
	return render_template("user_info.html", jobs=False)

@app.route("/user_infopost", methods=["POST"])
def user_infopost():
	session['location'] = request.form.get('location')
	if request.form.get('job_title'):
		session['job_title'] = request.form.get('job_title')
		session['job_description'] = request.form.get('job_description')
		session['wage'] = request.form.get('wage')
		session['start_date'] = request.form.get('start_date')

	print(session)
	return '{}'

@app.route("/success")
def success():
	return 'Success! We will contact you with information about a successful matching through Facebook Messenger soon.'
######################################################################################################


###################################################
#bot handling:
################################################### 

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message our bot, Facebook has implemented a verify token
        that confirms all requests that our bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        print('got GET')
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else: # request is POST
        # get whatever message a user sent the bot
        print('in POST block')
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                m = message.get('message')
                # this is an answer to a job posting
                if not bool(m):
                    p = message.get('postback')
                    print('not bool')
                    if p:
                        m = {'text':p['payload']}
                        print('pppppp')
                if m:
                    txt_received = m.get('text')
                    print('text_recived')
                    if txt_received:
                        recipient_id = message['sender']['id']
                        print('recipient_id: {}'.format(recipient_id))
                        #if accepting or rejecting a job
                        if txt_received.lower() == 'a' or txt_received.lower() == 'd':
                            print('about to call post_to_lavoro')
                            post_to_lavoro(txt_received.lower(), recipient_id, '12345678')
                            return "Message Processed"
                        #if any other message 
                        print('about to call post_to_lavoro')
                        post_to_lavoro(txt_received.lower(), recipient_id, '12345678')
                        return "Message Processed"

                        #translate text
                        #TODO: check if txt is not english
                        #transfer_to_translate(txt_received)
                        #post_to_lavoro('./translateFiles/vtext{}.txt'.format(num), id_to_phone.get(recipient_id))
                        #return "Message Processed"

                else:
                    print('not pricesd:')
                    return "NOT PROCESSED- no text present"
 

#this function sends a POST request to our backend, letting it know whether user
#wants a job or should have more offers sent 
def post_to_lavoro(signal, fb_UserID, jobPost_id):
    #sending accept/reject of a job offer
    print('post_to_lavoro succesfully caled')
    if not jobPost_id or not fb_UserID:
        #TODO: change the post address to our database end
        print('not jobPost_id or fb_UserID')
        #emulating our database:
        #lt = get_lavoro_text()
        return
    #emulating our database:
    #lt = get_lavoro_text()

    if signal is 'a':
        bol = True
    else:
        bol = False

    #TODO: make an actual request to our database
    r = requests.post('127.0.0.1:8000/history', json = {'accepted' : bol, 'job_id':jobPost_id,'user_id':fb_UserID})

# listen for lavoro text messages (job descriptions)
@app.route("/lavoro-new-job", methods=['POST'])
def get_lavoro_job():
    print('get_lavoro_job was called')
    if request.method == 'POST':
        print('request.method is POST')
        # get input message
        info = request.get_json()
        print(info)

        user_id = info['user_id']
        job_descr = info['job_description']
        job_id = info['job_id']
        lang = info['language']
        wage = info['job_wage']

        print('about to call send_fb_message')
        send_fb_message(user_id, info, 'newJob')
        return ('', 204)

# listen for lavoro text messages (job descriptions)
@app.route("/lavoro-accept-job", methods=['POST'])
def get_lavoro_acceptance():
    print('get_lavoro_acceptance was called')
    if request.method == 'POST':
        print('request.method is POST')
        # get input message
        info = request.get_json()
        print(info)

        #the poster in that case
        user_id = info['user_id']
        job_id = info['job_id']
        seeker_name = info['seeker_name']
        seeker_skills = info['seeker_skills']
        lang = info['language']

        print('about to call send_fb_message')
        send_fb_message(user_id, info, 'jobAccepted')
        return ('', 204)

# listen for lavoro text messages (job descriptions)
@app.route("/lavoro-reject-job", methods=['POST'])
def get_lavoro_rejection():
    print('get_lavoro_rejection was called')
    if request.method == 'POST':
        print('request.method is POST')
        # get input message
        info = request.get_json()
        print(info)

        user_id = info['user_id']
        lang = info['language']

        print('about to call send_fb_message')
        send_fb_message(user_id, info, 'jobRejected')
        return ('', 204)

# listen for lavoro text messages (job descriptions)
@app.route("/lavoro-new-connection", methods=['POST'])
def get_lavoro_match():
    print('get_lavoro_match was called')
    if request.method == 'POST':
        print('request.method is POST')
        # get input message
        info = request.get_json()

        user_id = info['user_id']
        lang = info['language']

        print('about to call send_fb_message')
        send_fb_message(user_id, info, 'newMatch')
        return ('', 204)

#uses PyMessenger to send response to user
def send_fb_message(recipient_id, response, msg_type):
    
    #sends user the text message provided via input response parameter
    print('send_fb_message was called succesfully')
    #TODO:
        #"text":response['job_description']
        #send job with accept/decline buttons:
    
    #Having the job descriptino implies that this is a new job offer msg
    if msg_type is 'newJob':
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
                    "text":"{}\n\n{}".format(msg ,job_desc),
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
    
    elif msg_type is 'jobAccepted':
        if response['langugage'] != 'en':
            #translate first argument into language in second argument
            msg = transfer_to_translate('We found you a potential employee!', response['langugage'])
            skills = transfer_to_translate(response['seeker_skills'], response['language'])
            acceptButt = transfer_to_translate('Hire!', response['langugage'])
            declineButt = transfer_to_translate('Show me other candidates', response['langugage'])
        else:
            msg = 'We found you a potential employee!'
            skills = response['seeker_skills']
            acceptButt = 'Hire!'
            declineButt = 'Show me other candidates'

        # construct payload and send it
        payload = {
        "recipient":{ "id":recipient_id},
        "message":{
                "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"{}\n\n candidate skills:{}".format(msg ,skills),
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

    elif msg_type is 'jobRejected':
        print('rejected job')
        return "success"

    elif msg_type is 'newMatch':
        if response['langugage'] != 'en':
                #translate first argument into language in second argument
                msg = transfer_to_translate('Yeah! You got the job!', response['langugage'])
                acceptButt = transfer_to_translate('Contact Employer!', response['langugage'])
                declineButt = transfer_to_translate('I dont want it', response['langugage'])
            else:
                msg = 'Yeah! You got the job!'
                acceptButt = 'Contact Employer!'
                declineButt = 'I dont want it'

         # construct payload and send it
        payload = {
        "recipient":{ "id":recipient_id},
        "message":{
                "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"{}\n".format(msg),
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



    bot.send_text_message(recipient_id, response)
    return "success"


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

#chooses a random message to send to the user (TESTING purposes ONLY)
def get_message():
    print('get_message was called succesfully')
    sample_responses = ["Message 1", "message 2", "message 3", "message 4"]
    # return selected item to the user
    return random.choice(sample_responses)
 
 
 
if __name__ == "__main__":
    app.run()

