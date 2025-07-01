from flask import Flask, request, send_from_directory, redirect, url_for, render_template
import os

# Expected GitHub token for uploads
EXPECTED_TOKEN = os.environ.get('GH_TOKEN')

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token = request.headers.get('GITHUB_TOKEN')
        if not token or token != EXPECTED_TOKEN:
            return 'Unauthorized', 403
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        return redirect(url_for('index'))
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)


@app.route('/files/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
