from flask import Blueprint
from flask_restful import Api
from deployment import server_status

deployment_bp = Blueprint('server_status', __name__)
api = Api(deployment_bp)

api.add_resource(server_status.Status, '/status')
