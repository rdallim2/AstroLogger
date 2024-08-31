from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

zipDict = {}

def makeZipDict(filename):
    global zipDict
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            key = parts[0]
            value = (float(parts[1].strip()), float(parts[2].strip()))  # Latitude and Longitude
            zipDict[key] = value


filename = 'zip-lat-lng.txt'
makeZipDict(filename)

@app.route('/')
def index():
    print("Index route was accessed.")
    return render_template('index.html')

#@app.route('/login')
#def login():

#def createAccount():
    


@app.route('/ziptocoords', methods=['POST'])
def ziptocoords():
    data = request.get_json()  # Get JSON data from request
    zip_code = data.get('zip_code')
    if zip_code:
        coords = zipDict.get(zip_code)
        if coords:
            return jsonify({"latitude": coords[0], "longitude": coords[1]})
        else:
            return jsonify({"error": "ZIP code not found"}), 404
    else:
        return jsonify({"error": "ZIP code not provided"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5996)