from flask import Flask, request, jsonify, render_template
import os
from extractor import extract_resume_data

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Extract data
    extracted_data = extract_resume_data(file_path)

    os.remove(file_path)

    return jsonify(extracted_data)

if __name__ == '__main__':
    app.run(debug=True)
from PyPDF2 import PdfReader

with open('sad.pdf', 'rb') as file:
    reader = PdfReader(file)
    number_of_pages = len(reader.pages)
    print(number_of_pages)
