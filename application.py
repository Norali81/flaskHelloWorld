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
    # This is an object of werkzeug.datastructures.FileStorage
    uploaded_file = request.files['image']
    filename = uploaded_file.filename
    

    if uploaded_file.filename != '':
        uploaded_file.save('./files/' + uploaded_file.filename)

        # The name of the image file to annotate
        file_path = os.path.abspath('./files/' + filename)
        print(file_path, file=sys.stderr)

        # Loads the image into memory
        with io.open(file_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Instantiates a client
        client = vision.ImageAnnotatorClient()

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        print('Labels:')
        for label in labels:
            print(label.description, file=sys.stdout)

    return render_template("image_result.html", filename=filename, file=content, labels=labels )

