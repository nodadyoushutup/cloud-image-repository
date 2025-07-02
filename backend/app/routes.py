import os
import hashlib
from flask import Blueprint, request, url_for, render_template, jsonify, redirect, session, current_app
from flask_dance.contrib.github import github

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    upload_folder = current_app.static_folder
    files = os.listdir(upload_folder)
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
    groups.reverse()

    github_user = None
    if github.authorized:
        resp = github.get("/user")
        if resp.ok:
            github_user = resp.json()

    return render_template('index.html', files=groups, github_conn=github, github_user=github_user)

@main_bp.route('/upload', methods=['POST'])
def upload():
    token = request.headers.get('CLOUD-REPOSITORY-APIKEY')
    expected = current_app.config.get('CLOUD_REPOSITORY_APIKEY')
    if not token or token != expected:
        return 'Unauthorized', 403
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    upload_folder = current_app.static_folder
    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    with open(filepath, 'rb') as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    sha_path = filepath + '.sha256'
    with open(sha_path, 'w') as sf:
        sf.write(digest)

    return jsonify({
        'path': url_for('static', filename=file.filename, _external=False),
        'sha256_file': url_for('static', filename=file.filename + '.sha256', _external=False),
        'sha256': digest
    })

@main_bp.route('/files/<path:filename>')
def uploaded_file(filename):
    # Redirect legacy /files routes to the static /public location
    return redirect(url_for('static', filename=filename))

@main_bp.route('/logout')
def logout():
    session.pop('github_oauth_token', None)
    return redirect(url_for('main.index'))

@main_bp.route('/delete/<path:filename>', methods=['POST'])
def delete_file(filename):
    if not github.authorized:
        return 'Unauthorized', 403
    safe_name = os.path.basename(filename)
    upload_folder = current_app.static_folder
    path = os.path.join(upload_folder, safe_name)
    sha_path = path + '.sha256'
    if os.path.exists(path):
        os.remove(path)
    if os.path.exists(sha_path):
        os.remove(sha_path)
    return redirect(url_for('main.index'))
