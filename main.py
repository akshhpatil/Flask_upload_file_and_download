import os
from flask import Flask, render_template, request, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename

# upload file1
UPLOAD_DIRECTORY = "E:/Flask_file_demo/uploads/data"

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'csv', 'xlsx'])



app = Flask(__name__)
app.secret_key = 'SECURE'

app.config['UPLOAD_DIRECTORY'] = UPLOAD_DIRECTORY



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# download all files function
@app.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@app.route('/')
def upload():
    return render_template('upload_file.html')


# Upload all types of files into folder
@app.route('/upload', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_DIRECTORY'], filename))
        flash('File(s) successfully uploaded','success')
        return render_template('upload_file.html')

@app.route('/files')
def files():

        files = []
        for filename in os.listdir(UPLOAD_DIRECTORY):
            path = os.path.join(UPLOAD_DIRECTORY, filename)
            if os.path.isfile(path):
                files.append(filename)

        return render_template('showfiles.html', files=files)



app.run(debug=True)
