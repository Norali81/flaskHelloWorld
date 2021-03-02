from flask import Flask, render_template, request
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud import storage

import sys
import io
import os

app= Flask(__name__)

def upload_blob(bucket_name, source_file_name, destination_blob_name, path_to_file):
    """Uploads a file to the bucket."""
    bucket_name = "flaskimages"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

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
        
    # save file to disk 
    if uploaded_file.filename != '':
    #    uploaded_file.save('./files/' + uploaded_file.filename)

        # The name of the image file to annotate
        #file_path = os.path.abspath('./files/' + filename)
        #print(file_path, file=sys.stderr)

        # Loads the image into memory
        #with io.open(file_path, 'rb') as image_file:
        #    content = image_file.read()

        # https://stackoverflow.com/questions/7368061/how-to-reset-the-file-stream-in-flask-werkzeug
        #uploaded_file.stream.seek(0)
        content = uploaded_file.stream.read()

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

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)