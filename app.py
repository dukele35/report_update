import os
from flask import Flask, request, redirect, flash, jsonify
from werkzeug.utils import secure_filename
from ultis import *

app = Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['json'])
app.config.update(SECRET_KEY=os.urandom(24))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["POST"])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        all_predictions = {}
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                data_owner = json_to_dict(filename)
                all_predictions.update(data_owner)
        performance = sen_spec(data_owner)
        return jsonify(performance)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')