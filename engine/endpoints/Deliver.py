from flask import jsonify
from flask_restful import Resource, reqparse
from endpoints import Auxiliary


class Deliver(Resource):
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        """"Returns the study template.

            Returns the template of the indicated study only if the indicated user owns that study.

            Args:
                token (String): A tokenized identifier of a user, tokenization is done with
                                a flask GET HTTP request using the crypto blueprint and formatted like this.
                                ('/token/generate', data={'user_id': 'VALID_USER_IN_DATABASE'})
                                
                study_id (int): The identifier for the study the user is trying to download.

            Returns:
                JSON: The desired study template, or an error message.
            """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        #parser.add_argument("user_id", type=str, required=True, help="The user ID of the owner is a String.")
        parser.add_argument("study_id", type=int, required=True, help="The study ID of the owned study is an integer.")
        returned_args = parser.parse_args()
        user_id = kwargs["user_id"]  #returned_args.get("user_id", None)
        study_id = returned_args.get("study_id", None)
        # return the study template only if owned
        if Auxiliary.isOwned(user_id, study_id):
            return Auxiliary.getTemplate(study_id)
        else:
            return jsonify({"error": "user does not own study"})
