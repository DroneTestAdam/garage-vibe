# app.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GITHUB_TOKEN = '605134429551'
REPO_OWNER = 'DroneTestAdam'
REPO_NAME = 'garage-vibe'
FILE_PATH = 'status.txt'

@app.route('/update_status', methods=['POST'])
def update_status():
    status = request.json.get('status')
    if status not in [
        "Actively being used, just stop by!",
        "Open - I’m just not in garage yet",
        "Closed - The Professor Only"
    ]:
        return jsonify({'error': 'Invalid status - Adam probably knows and doesnt want to fix it right now.'}), 400

    url = f'http://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}

    # Get the SHA of the existing file
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()['sha']
    else:
        return jsonify({'error': 'Could not get file SHA'}), 500

    # Update the file
    content = status.encode('utf-8').decode('utf-8')
    data = {
        "message": f"Update status to {status}",
        "content": content.encode('base64'),
        "sha": sha
    }
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        return jsonify({'message': 'Status updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update status'}), 500

if __name__ == '__main__':
    app.run()