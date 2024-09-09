from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
from bson import ObjectId
import uuid
from gridfs import GridFS

user_collection = db.users

class User:
    def __init__(self, db):
        self.db = db

    def start_session(self, user):
        del user['password'] #don't want password saved in user object
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        print(request.form)

        #Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        
        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        #check for existing email
        if db.users.find_one({ "email": user['email']}):
            return jsonify({ "error": "Email address already in use."}), 400
        print("sending to db")

        if db.users.insert_one(user):
            return self.start_session(user)
            #return jsonify(user), 200

        return jsonify({ "error": "Signup failed" }), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):

        user = db.users.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        
        return jsonify({ "error": "Invalid login credentials" }), 401

    def submit_data(self):
        data_collection = self.db['user_data'] 
        fs = GridFS(db)

        data = {
           'observationProgram': request.form.get('observationProgram'),
           'objectName': request.form.get('inlineFormObjectName'),
           'latitude': request.form.get('inlineFormLatitude'),
           'longitude': request.form.get('inlineFormLongitude'),
           'date': request.form.get('inlineFormDate'),
           'time': request.form.get('inlineFormTime'),
           'seeing': request.form.get('inlineFormSeeing'),
           'transparency': request.form.get('inlineFormTransparency'),
           'size': request.form.get('inlineFormSize'),
           'filters': request.form.get('inlineFormFilters'),
           'description': request.form.get('description'),
           'power': request.form.get('power'),
        }
        if 'image' in request.files:
           image = request.files['input-file']
           if image and image.filename:
               filename = str(uuid.uuid4()) + '.' + image.filename.rsplit('.', 1)[1].lower()
               file_id = fs.put(image, filename=filename)
               data['image_file_id'] = str(file_id)
        result = db.user_data.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return jsonify({"message": "Submission successful", "data": data}), 200
