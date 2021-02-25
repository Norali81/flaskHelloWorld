from flask import Flask, render_template, request
# Imports the Google Cloud client library
from google.cloud import vision
import sys
import io
import os

app= Flask(__name__)

@app.route("/")
def index():
    name = request.args.get("name")
    return render_template("index.html", name=name)

@app.route("/submit" , methods=["POST"])
def submit():
    fname = request.form.get("fname")
    lname = request.form.get("lname") 
    if not fname or not lname:
        return "Failiure"

    return render_template("success.html", fname=fname, lname=lname)

@app.route("/image")
def image():
    return render_template("image.html")

@app.route("/image_result", methods=["POST"])
def image_result():
    uploaded_file = request.files['image']
    filename = uploaded_file.filename
    

    if uploaded_file.filename != '':
        print('This is error output', file=sys.stderr)
        print('This is standard output', file=sys.stdout)
        uploaded_file.save(uploaded_file.filename)

    return render_template("image_result.html", filename=filename, file=uploaded_file )

