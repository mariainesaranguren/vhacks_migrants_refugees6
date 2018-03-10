from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
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
	json = request.json
	session['facebook_id'] = json['id']
	session['first_name'] = json['first_name']
	session['last_name'] = json['last_name']
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
		session['job_name'] = request.form.get('job_title')
		session['job_description'] = request.form.get('job_description')
		session['job_wage'] = request.form.get('wage')
		session['job_date'] = request.form.get('start_date')
		requests.post('http://localhost:8000/jobs/', data=dict(session))
	else:
		requests.post('http://localhost:8000/seekers/', data=dict(session))

	print(session)

	return '{}'

@app.route("/success")
def success():
	return 'Success! We will contact you with information about a successful matching through Facebook Messenger soon.'

@app.route("/success_test")
def success_test():
	print(session)
	requests.post('http://localhost:8000/jobs/', data = {'job_wage': '12.00', 'first_name': 'Vinay', 'job_description': 'Some cool description', 'location': 'New York, NY, USA', 'facebook_id': '2058520710831813', 'job_name': 'Some cool Job', 'skills': ['Accountant', 'Cook', 'Driver'], 'last_name': 'Khemlani', 'language': 'IT', 'job_date': '1/10/30'})
	# requests.post('http://localhost:8000/seekers/', data = {'first_name': 'Vinay', 'language': 'IT', 'skills': ['Accountant'], 'location': 'New York, NY, USA', 'facebook_id': '2058520710831813', 'last_name': 'Khemlani'})
	return 'Success test'