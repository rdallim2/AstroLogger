from flask import Flask
from app import app #from app.py import app
from user.models import User #from user dir, models file, import User class 

@app.route('/user/signup', methods=['GET'])
def signup():
    return User().signup() #creating new class instance

