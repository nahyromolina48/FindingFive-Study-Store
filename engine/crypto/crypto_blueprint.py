from flask import Blueprint
from flask_restful import Api
from crypto import GuiToken

crypto_bp = Blueprint('crypto', __name__)
api = Api(crypto_bp)

api.add_resource(GuiToken.Generator, '/token/generate')
