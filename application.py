from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/role")
def roles():
	return render_template("role.html")

@app.route("/skills")
def skills():
	return render_template("skills.html")