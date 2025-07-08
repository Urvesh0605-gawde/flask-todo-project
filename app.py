from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from dotenv import load_dotenv
import os, json
from pymongo.mongo_client import MongoClient  # import MongoClient for MongoDB

app = Flask(__name__)
app.secret_key = 'your_secret_key'
load_dotenv()

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


@app.route("/api")
def api():
    with open("data.json") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        if not name or not email:
            flash("All fields are required.")
            return render_template("form.html")

        try:
            collection.insert_one({"name": name, "email": email})
            return redirect(url_for("success"))
        except Exception as e:
            flash(f"Error: {e}")
            return render_template("form.html")

    return render_template("form.html")

@app.route("/success")
def success():
    return render_template("success.html")
