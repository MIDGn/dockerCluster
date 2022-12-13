"""Modeule socket to get hostname"""
import socket
import os
from datetime import datetime
from pymongo import MongoClient
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = MongoClient('mongo', 27017)
database = client["test_database"]
collection = database.collection

if not collection.count_documents({"value": 0}):
    counter_init_ = {"value": 0}
    collection.insert_one(counter_init_)

@app.route('/')
def show_stat():
    """Return value of counter"""
    counter = collection.find().sort('value', -1)[0]
    result = str(counter["value"])
    return result

@app.route('/stat')
def increment():
    """Increase value of counter by 1, add data to database"""
    current_counter = collection.find().sort('value', -1)[0]
    current_datetime = datetime.now()
    client_info = request.user_agent
    collection.insert_one({
        "value": current_counter["value"]+1,
        "datetime": current_datetime,
        "client_info": str(client_info),
    })
    next_value = current_counter["value"] + 1
    result = str(next_value) + ' -- ' + str(current_datetime) + ' -- ' + str(client_info)
    return result


@app.route('/about')
def hello():
    """HA, GREETINGS"""
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"
    return html.format(name="Георгий", hostname=socket.gethostname())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("SERVER_PORT", 8080), debug=True)
 