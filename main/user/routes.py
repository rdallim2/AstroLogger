from flask import Flask, render_template, request, Response
from bson.objectid import ObjectId
from gridfs import GridFS
from app import app, db #from app.py import app
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

@app.route('/submit_data', methods=['POST'])
def submit_data_route():
    user = User(db)
    return user.submit_data()


@app.route('/myLogs')
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
