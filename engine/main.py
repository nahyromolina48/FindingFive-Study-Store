from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from crypto.PublicTokenGenerator import TokenService
from endpoints import transaction_blueprint as tbp
from crypto import crypto_blueprint as cbp
from deployment import deployment_blueprint as dbp
from exceptions import Authentication as auth

app = Flask(__name__)
app.register_blueprint(tbp.trans_bp)
app.register_blueprint(cbp.crypto_bp)
app.register_blueprint(dbp.deployment_bp)
app.register_error_handler(401, auth.handle_auth)
app.register_error_handler(501,auth.malformed_url_query)
app.register_error_handler(500,auth.generic_exception)
CORS(app)
api = Api(app)


class TokenCreation(Resource):
    # maybe should be a post to test thDK Ie client
    def get(self):
        ts = TokenService()
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("user_id", type=str)
        # string representation of ints
        parser.add_argument("user_type", type=str)
        parser.add_argument("credits", type=str)
        parser.add_argument("hash", type=str)
        parser.add_argument("nonce", type=str)
        returned_args = parser.parse_args()
        print(returned_args)
        msg_validty, vals = ts.verify_msg(returned_args)
        resp = {'valid': msg_validty, "vals": vals, "old": returned_args}
        return jsonify(resp)


api.add_resource(TokenCreation, '/tokenCreation')

if __name__ == '__main__':
    # runs on localhosts
    app.run(host='129.3.20.26', port=12100, debug=True)
