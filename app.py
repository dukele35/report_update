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

@app.route("/start", methods=["POST"])
def upload_uuid():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uuid = json_to_dict(filename)['uuid']
            os.mkdir(os.path.join(UPLOAD_FOLDER, uuid))
            file.save(os.path.join(UPLOAD_FOLDER, uuid, filename))
            response = {'response': f'a folder named {uuid} is created'}
            return jsonify(response)

@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        all_predictions = {}
        for file in files:
            if file and allowed_file(file.filename):
                if 'uuid' in file.name: 
                    filename = secure_filename(file.filename)
                    uuid = json_to_dict(filename)['uuid']
                if 'prediction' in file.name:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, uuid, filename))
                    response = {'response': f'the {filename} is saved in the {uuid} folder'}
                    return jsonify(response)

@app.route("/report", methods=["POST"])
def create_report():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uuid = json_to_dict(filename)['uuid']
            dir = os.listdir(os.path.join(UPLOAD_FOLDER, uuid))
            all_preds = {}
            for f in dir:
                if 'prediction' in f:
                    pred = json_to_dict(f)
                    all_preds.update(pred)
            performance = sen_spec(pred)
            os.chdir(os.path.join(UPLOAD_FOLDER, uuid))
            json_outputing(performance,'performance.json')
            return jsonify(performance)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')