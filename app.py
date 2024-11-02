import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

# flask app set up
app = Flask(__name__)

# store images uploaded
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# allowed extensions for image files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# check if a file name is well formated (png or jpg)
def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True
    return False

# main home page, GET is to see the web page, POST is trigger the deshredding process
@app.route("/", methods=["GET", "POST"])
def deshred():

    if request.method == "POST":

        # option 1: the add fragment button was pressed
        if 'add_image' in request.form:

            # check that a file was uploaded first
            if 'image' not in request.files:
                return render_template("index.html", error="No file uploaded", images=[])
            
            # get the image uploaded and save it
            file = request.files['image']
            if file and allowed_file(file.filename):

                # create a secure version of the file name
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

    # render current images
    current_images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("index.html", images=current_images)

if __name__ == "__main__":
    app.run(debug=True)
