from flask import Flask, render_template, request
from app import app #from app.py import app
from user.models import User #from user dir, models file, import User class 

@app.route('/user/signup', methods=['POST'])
def signup():
    # Handle the form submission, e.g., by calling the User class's signup method.
    print("Processing signup form submission.")
    return User().signup()

@app.route('/user/signout')
def signout():
    return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
    return User().login()