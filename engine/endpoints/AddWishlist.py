from flask import jsonify
from flask_restful import Resource, reqparse
from endpoints import Auxiliary


class AddWishlist(Resource):
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        """"Adds the study to the user's wish list.

        Establishes a wish lists relationship between a study and a user.

        Args:
            token (String): A tokenized identifier for the user wish listing the study, tokenization is done with
                            a flask GET HTTP request using the crypto blueprint and formatted like this.
                            ('/token/generate', data={'user_id': 'VALID_USER_IN_DATABASE'})
                            
            study_id (int): The identifier for the study the user is trying to wish list.

        Returns:
            JSON: {"Success": True}
        """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        #parser.add_argument("user_id", type=str, required=True, help="The user ID of the wish lister is a String.")
        parser.add_argument("study_id", type=int, required=True,
                            help="The study ID of the study being wish listed is an integer.")
        returned_args = parser.parse_args()
        user_id = kwargs["user_id"]  #returned_args.get("user_id", None)
        study_id = returned_args.get("study_id", None)

        # update the user data
        Auxiliary.addWishlist(user_id, study_id)
        # return success
        return jsonify({"Success": True})
