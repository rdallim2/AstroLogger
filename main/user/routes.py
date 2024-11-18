from flask import Flask, render_template, request, Response
import pymongo
from bson.objectid import ObjectId
from gridfs import GridFS
from app import app, db, login_required #from app.py import app
from user.models import User #from user dir, models file, import User class 

@app.route('/user/signup', methods=['POST'])
def signup():
    # Handle the form submission, e.g., by calling the User class's signup method.
    print("Processing signup form submission.")
    return User(db).signup()

@app.route('/user/signout')
def signout():
    return User(db).signout()

@app.route('/user/login', methods=['POST'])
def login():
    return User(db).login()

@app.route('/submit_data', methods=['POST'])
def submit_data_route():
    user = User(db)
    return User(db).submit_data()


@app.route('/myLogs')
@login_required
def retrieve_data_route():
    print ("myLogs route was accessed.")
    user = User(db)
    return user.retrieve_data()

# Serve images based on their GridFS ObjectId
@app.route('/image/<image_id>')
def serve_image(image_id):
    print(f"Received image_id: {image_id}, heres all the files in fs.files")
    fs = GridFS(db)

    try:
        file_id = ObjectId(image_id)
        grid_out = fs.get(file_id)
        print(f"Received image_id: {image_id}, Converted to ObjectId: {file_id}")
        return Response(grid_out.read(), mimetype='image/jpeg')
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}", 404
