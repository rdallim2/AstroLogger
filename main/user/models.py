from flask import Flask, jsonify, request, session, redirect, render_template, url_for
from passlib.hash import pbkdf2_sha256
from app import db
from bson import ObjectId
import uuid
from gridfs import GridFS
import pymongo


try:
    client = pymongo.MongoClient("mongodb://mongodb:27017/")
    db = client.user_login_system
    user_collection = db.users
    # Test if the connection is successful
    client.admin.command('ping')  # Sends a ping command to test the connection
    print("MongoDB connection successful")
except ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")


class User:
    def __init__(self, db):
        self.db = db


    def start_session(self, user):
        del user['password'] #don't want password saved in user object
        session['logged_in'] = True
        session['user_id'] = user['_id']
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
            'user_id': session['user']['_id'],
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
            'power': request.form.get('power')
        }
        if 'visual-input-file' in request.files:
            image = request.files['visual-input-file']
            if image and image.filename:
                print(f"Image uploaded: {image.filename}")
                filename = request.files['visual-input-file']
                filename = str(uuid.uuid4()) + '.' + image.filename.rsplit('.', 1)[1].lower()
                file_id = fs.put(image, filename=filename)
                print(f"File ID: {file_id}")  # Log file ID
                data['visual_image_file_id'] = str(file_id)
        
        if 'imaging-input-file' in request.files:
            image = request.files['imaging-input-file']
            if image and image.filename:
                print(f"Image uploaded: {image.filename}")
                filename = request.files['imaging-input-file']
                filename = str(uuid.uuid4()) + '.' + image.filename.rsplit('.', 1)[1].lower()
                file_id = fs.put(image, filename=filename)
                print(f"File ID: {file_id}")  # Log file ID
                data['imaging_image_file_id'] = str(file_id)
        else:
            print("No image found in the request")
        result = data_collection.insert_one(data)
        data['_id'] = str(result.inserted_id)

        return redirect(url_for('retrieve_data_route'))

    def retrieve_data(self):
        data_collection = self.db['user_data'] 
        logs = data_collection.find()

        data = []

        for doc in logs:
            doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
            if 'image_file_id' in doc:
                doc['image_file_id'] = str(doc['image_file_id']) 
            data.append(doc)


        return render_template('myLogs.html', data=data)



    #def retrieve_data(self):
