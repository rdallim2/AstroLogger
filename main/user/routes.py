from flask import Flask, render_template, request
from app import app #from app.py import app
from user.models import User #from user dir, models file, import User class 

@app.route('/user/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle the form submission, e.g., by calling the User class's signup method.
        print("Processing signup form submission.")
        return User().signup()
    else:
        # Render the signup form.
        print("Rendering signup form.")
        return render_template('signup.html')

@app.route('/user/signout')
def signout():
    return User().signout()



