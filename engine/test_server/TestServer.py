import binascii
import hashlib as hl
import os
import requests as req
from nacl import secret, utils
import base64
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class ClientServer(Resource):
    """
    This is to represent what a user process or connection will look like.
    """
    dummy_user = {"user_id": 'kazookid', "user_type": 2, "credits": 200}

    def __init__(self):
        self.secret_key = self.load_secret_key()

    def encrypt_fields(self, nonce):
        box = secret.SecretBox(self.secret_key)
        self.dummy_user["user_id"] = box.encrypt((self.dummy_user["user_id"]).encode('utf-8'), nonce)
        self.dummy_user["user_type"] = box.encrypt(self.dummy_user["user_type"].to_bytes(2, byteorder="little"), nonce)
        self.dummy_user["credits"] = box.encrypt(self.dummy_user["credits"].to_bytes(2, byteorder="little"), nonce)
        self.dummy_user['nonce'] = nonce

    def convert_to_base64(self):
        self.dummy_user["user_id"] = base64.encodebytes(self.dummy_user["user_id"]).decode('ascii')
        self.dummy_user["user_type"] = base64.encodebytes(self.dummy_user["user_type"]).decode('ascii')
        self.dummy_user["credits"] = base64.encodebytes(self.dummy_user["credits"]).decode('ascii')
        self.dummy_user["nonce"] = base64.encodebytes(self.dummy_user["nonce"]).decode('ascii')

    def load_secret_key(self):
        env_path = os.path.abspath(os.path.dirname(__file__))
        location = os.path.join(env_path, '.env')
        load_dotenv(dotenv_path=location)
        # load_dotenv('../Crypto/secrets.env')
        secret_key = os.getenv('SECRET')
        if secret_key is None:
            server_key = self.create_keys(location)
            return server_key
        return base64.decodebytes(secret_key.encode('ascii'))

    def generate_nonce(self):
        return utils.random(secret.SecretBox.NONCE_SIZE)

    def create_keys(self, location):
        # create the server key  and stores in a local file.
        server_key = utils.random(secret.SecretBox.KEY_SIZE)
        with open(location, "a") as f:
            f.write("SECRET=")
            f.write(base64.encodebytes(server_key).decode('ascii'))
        return server_key

    def get(self):
        # to test the client getting the token
        url = "http://localhost:5000/tokenCreation"
        dummy_hash = hl.sha256()
        nonce = self.generate_nonce()
        self.encrypt_fields(nonce)
        dummy_hash.update(
            binascii.hexlify(self.dummy_user["user_id"] + self.dummy_user["user_type"] + self.dummy_user["credits"]))
        self.dummy_user["hash"] = dummy_hash.hexdigest()
        self.convert_to_base64()
        data = self.dummy_user
        response = req.get(url, json=data)
        if "application/json" in response.headers['content-type']:
            return response.json()
        return response.content

def test_queue(self):
    i=0
    for i in range(200):
        i = i*2

api.add_resource(ClientServer, '/simulate')

if __name__ == '__main__':
    # runs on localhosts
    app.run(host='0.0.0.0', debug=True, port="6868")
