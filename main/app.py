from flask import Flask, render_template

app = Flask(__name__)

zipDict = {}

def makeZipDict(filename):
    global zipDict
    with open (file, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            key = parts[0]
            value = (int(parts[1].strip()), parts[2].strip())
            zipDict[key] = value

filename = zip-lat-lng.txt
makeZipDict(filename)

@app.route('/')
def index():
    print("Index route was accessed.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5996)