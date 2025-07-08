from flask import Flask, request, render_template  # import flask
from datetime import datetime  # import datetime
from dotenv import load_dotenv  # import load_dotenv to load environment variables
import os  # import os to access environment variables
from pymongo.mongo_client import MongoClient  # import MongoClient for MongoDB

load_dotenv()  # load the environment variables from .env file

MONGO_URL = os.getenv('MONGO_URL')  # get the MongoDB connection string from environment variables

# Create a new client and connect to the server
client = MongoClient(MONGO_URL)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['test']  # replace with your database name

collection = db['flask_tutorials']  # replace with your collection name

app = Flask(__name__)  # create an application

@app.route('/')  # define the home route
def home():
    day_of_week = datetime.now().strftime('%A')
    currnt_time = datetime.now().strftime('%H:%M:%S')
    return render_template('index.html', day_of_week=day_of_week, currnt_time=currnt_time)  # render the index.html file

@app.route('/submit', methods=['POST'])  # define the submit route
def submit():
    form_data = dict(request.form)  # get the form data as a dictionary
    collection.insert_one(form_data)  # insert the form data into the MongoDB collection
    return 'Data submitted successfully'  # return the form data as a response

@app.route('/view')  # define the data route
def view():
    data_cursor = collection.find()  # retrieve all documents from the MongoDB collection
    data_list = []
    for item in data_cursor:
        item.pop('_id', None)  # remove the '_id' field from each document for cleaner output
        data_list.append(item)
    return {'data': data_list}  # return the data as JSON

# @app.route('/api/<name>')  # define the home route
# def name(name):
#     length = len(name)
#     if length > 5:
#         return 'Name is too long'
#     else:
#         return 'Nice Name'
#     result = 'Hello ' + name + '!'
#     return result

# @app.route('/add/<a>/<b>')  # define the home route
# def add(a, b):
#     answer = int(a) + int(b)
#     result = {
#         "ans": answer
#     }
#     return result

if __name__ == '__main__':  # this is imp to run flask application
    app.run(debug=True, port=5002)  # using debug to apply the changes
