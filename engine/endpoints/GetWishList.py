from flask import jsonify
from flask_restful import Resource, reqparse
from endpoints import Auxiliary


class GetWishList(Resource):
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        """"Returns the list of .wishList studies by a user.

        Returns the wish list of studies saved by a user.

        Args:
            token (String): A tokenized identifier of a user, tokenization is done with
                                a flask GET HTTP request using the crypto blueprint and formatted like this.
                                ('/token/generate', data={'user_id': 'VALID_USER_IN_DATABASE'})

        Returns:
            JSON: The wish list of studies.
        """

        parser = reqparse.RequestParser(bundle_errors=True)
        #parser.add_argument("user_id", type=str, required=True, help="The user ID of the viewer is a String.")
        returned_args = parser.parse_args()
        user_id = kwargs["user_id"]  #returned_args.get("user_id", None)
        # print(returned_args)
        user = Auxiliary.getUser(user_id)
        search = user.get_wishList()
        params = {"Study_id": {"$in": search}}
        studyList = Auxiliary.getStudies(params)
        # convert output
        out = Auxiliary.studyListToDictList(studyList)
        # return converted output
        return jsonify(out)
