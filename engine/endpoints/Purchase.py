from flask import jsonify
from flask_restful import Resource, reqparse
from endpoints import Auxiliary


class Purchase(Resource):
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        """"Establishes an owns relationship between a study and a user.

            Establishes the owns relationship only if the user has sufficient credits and doesn't already own the study.

            Args:
            
                token (String): A tokenized identifier of a user, tokenization is done with
                                a flask GET HTTP request using the crypto blueprint and formatted like this.
                                ('/token/generate', data={'user_id': 'VALID_USER_IN_DATABASE'})
                                
                study_id (int): The identifier for the study the user is trying to purchase.
                
                credits_available (int): The current credit balance for the user. Overrides any stored balance.

            Returns:
                JSON: The cost of the study, or an error message.
            """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        #parser.add_argument("user_id", type=str, required=True, help="The user ID of the customer is a String.")
        parser.add_argument("study_id", type=int, required=True,
                            help="The study ID of the study being purchased is an integer.")
        parser.add_argument("credits_available", type=int, required=True,
                            help="The credit balance available to the customer is an integer.")
        returned_args = parser.parse_args()
        user_id = kwargs["user_id"]  #returned_args.get("user_id", None)
        study_id = returned_args.get("study_id", None)
        credits_available = returned_args.get("credits_available", None)
        # verify the parameters exist - now handled by add_argument
        # if user_id == None or study_id == None or credits_available == None:
        #    return jsonify({"error": "missing parameter"})
        # get the necessary data from the database
        user = Auxiliary.getUser(user_id)
        # check for ownership first, because credits won't matter if already owned
        if study_id in user.get_ownedStudies():
            return jsonify({"cost": 0})
        study = Auxiliary.getStudy(study_id)
        cost = study.get_costInCredits()
        # check for sufficient credits and not already owning the study
        if cost > credits_available:
            return jsonify({"error": "insufficient credits"})
        # update the user data
        Auxiliary.addOwned(user_id, study_id, cost)
        # return the cost
        return jsonify({"cost": cost})
