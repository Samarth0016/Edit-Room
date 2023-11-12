from flask import Flask, render_template, request, flash , request, redirect, url_for
import cv2
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif', 'webp'}


app = Flask(__name__)

app.secret_key = 'the random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename, Operation):
     print(f"filename is {filename} and operation is {Operation}")
     image = cv2.imread(f"uploads/{filename}")
     match Operation:
          case "convertgrey":
               gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
               newFilename = f"static/{filename}"
               cv2.imwrite(newFilename,image)
               cv2.imwrite(newFilename, gray)
               return newFilename

          case "convertpng":
               newFilename = f"static/{filename.split('.')[0]}.png"
               cv2.imwrite(newFilename, image)
               return newFilename
          
          case "convertwebp":
               newFilename = f"static/{filename.split('.')[0]}.webp"
               cv2.imwrite(newFilename, image)
               return newFilename
          
     


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
        if request.method== "POST":
            Operation = request.form.get("Operation")

            if 'file' not in request.files:
                return('No file part')
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                return ('No selected file')
                
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new= processImage(filename, Operation)
                flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
                return render_template("index.html")

        return render_template("index.html")
app.run(debug=True)