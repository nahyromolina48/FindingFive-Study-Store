from flask import Blueprint
from flask_restful import Api
from endpoints.Deliver import Deliver
from endpoints.Purchase import Purchase
from endpoints.Search import Search
from endpoints.IsOwned import IsOwned
from endpoints.GetOwned import GetOwned
from endpoints.GetViewed import GetViewed
from endpoints.GetWishList import GetWishList
from endpoints.Upload import Upload
from endpoints.GetAdminDetails import GetAdminDetails
from endpoints.GetPending import GetPending
from endpoints.ReviewPending import ReviewPending
from endpoints.GetPreview import GetPreview
from endpoints.suggestions import TextSuggestion
from endpoints.AddWishlist import AddWishlist
from endpoints.RemoveWishlist import RemoveWishlist
from endpoints.IsWishlisted import IsWishlisted
from endpoints.RateStudy import RateStudy
from endpoints.GetNotifications import GetNotifications
from endpoints.Unpublish import Unpublish
from endpoints.CheckToken import CheckToken

trans_bp = Blueprint('transaction', __name__)
api = Api(trans_bp)

api.add_resource(Deliver, '/deliver')
api.add_resource(Purchase, '/purchase')
api.add_resource(Search, '/search')
api.add_resource(IsOwned, '/isOwned')
api.add_resource(GetOwned, '/getOwned')
api.add_resource(GetViewed, '/getViewed')
api.add_resource(GetWishList, '/getWishlist')
api.add_resource(Upload, '/upload')
api.add_resource(GetAdminDetails, '/getAdminDetails')
api.add_resource(GetPending, '/getPending')
api.add_resource(ReviewPending, '/reviewPending')
api.add_resource(GetPreview, '/getPreview')
api.add_resource(TextSuggestion, '/suggestion')
api.add_resource(AddWishlist, '/addWishlist')
api.add_resource(RemoveWishlist, '/removeWishlist')
api.add_resource(IsWishlisted, '/isWishlisted')
api.add_resource(RateStudy, '/rateStudy')
api.add_resource(GetNotifications, "/getNotifications")
api.add_resource(Unpublish, "/unpublish")
api.add_resource(CheckToken, "/checkToken")