from flask import (
    Flask,
    request,
    send_from_directory,
    url_for,
    render_template,
    jsonify,
    redirect,
    session,
)
from flask_dance.contrib.github import make_github_blueprint, github
import os
import hashlib

# Expected GitHub token for uploads
EXPECTED_TOKEN = os.environ.get('CLOUD_REPOSITORY_APIKEY')
GITHUB_OAUTH_CLIENT_ID = os.environ.get(
    'GITHUB_OAUTH_CLIENT_ID', "Ov23ligIOwzpGYVkuvyu")
GITHUB_OAUTH_CLIENT_SECRET = os.environ.get(
    'GITHUB_OAUTH_CLIENT_SECRET', "5e823eef5497b276ea4679383217ecb9a912876e")

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'secret')
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# GitHub OAuth setup
github_bp = make_github_blueprint(
    client_id=os.environ.get("GITHUB_OAUTH_CLIENT_ID"),
    client_secret=os.environ.get("GITHUB_OAUTH_CLIENT_SECRET"),
)
app.register_blueprint(github_bp, url_prefix="/login")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token = request.headers.get('CLOUD-REPOSITORY-APIKEY')
        if not token or token != EXPECTED_TOKEN:
            return 'Unauthorized', 403
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Calculate sha256 and store alongside the uploaded file
        with open(filepath, 'rb') as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        sha_path = filepath + '.sha256'
        with open(sha_path, 'w') as sf:
            sf.write(digest)

        return jsonify({
            'path': url_for('uploaded_file', filename=file.filename, _external=False),
            'sha256_file': url_for('uploaded_file', filename=file.filename + '.sha256', _external=False),
            'sha256': digest
        })
    files = os.listdir(UPLOAD_FOLDER)
    groups = []
    file_set = set(files)
    for f in sorted(files):
        if f.endswith('.sha256'):
            continue
        sha_name = f + '.sha256'
        groups.append({
            'image': f,
            'sha256': sha_name if sha_name in file_set else None
        })
    return render_template('index.html', files=groups, logged_in=github.authorized)


@app.route('/files/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/logout')
def logout():
    session.pop('github_oauth_token', None)
    return redirect(url_for('index'))


@app.route('/delete/<path:filename>', methods=['POST'])
def delete_file(filename):
    if not github.authorized:
        return 'Unauthorized', 403
    safe_name = os.path.basename(filename)
    path = os.path.join(UPLOAD_FOLDER, safe_name)
    sha_path = path + '.sha256'
    if os.path.exists(path):
        os.remove(path)
    if os.path.exists(sha_path):
        os.remove(sha_path)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
