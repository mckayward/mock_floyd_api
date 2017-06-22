from flask import Flask, json, request
import random
from redis import Redis
import string

app = Flask(__name__)
redis_client = Redis()  # Defaults are host='localhost', port=6379

def random_id(n=22):
    """
    Generates a random string consisting of uppercase letters,
    lowercase letters, and numbers
    """
    return ''.join(random.SystemRandom().choice(string.ascii_letters +
        string.digits) for _ in range(n))

@app.route('/api/v1/completed_upload/', methods=['POST'])
def completed_upload():
    id = json.loads(request.data)["ID"]
    print("Start untarring for {}".format(id))
    return ""

@app.route('/api/v1/cli_version/')
def cli_version():
    return json.jsonify({"min_version": "0.9.2", "latest_version": "0.9.2"})

@app.route('/api/v1/upload_succeeded/', methods=['POST'])
def success():
    return "success"

@app.route('/api/v1/upload_failed/', methods=['POST'])
def failure():
    return "failure recorded"

@app.route('/api/v1/modules/', methods=['POST'])
def modules():
    # Just return an ID
    return json.jsonify(id=random_id())

@app.route('/api/v1/modules/new_credentials/', methods=['POST'])
def data_creds():
    # TODO: Auth before granting token
    id = json.loads(request.data)["id"]

    # TODO: This could be a more secure token
    token = random_id(50)
    redis_client.setex(id, token, 7200)  # 2 Hours

    return json.jsonify({"id": id, "token": token})

if __name__ == "__main__":
    app.run(port=8080)
