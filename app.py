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
    app.run()
