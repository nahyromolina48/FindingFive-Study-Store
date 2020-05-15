from flask import jsonify
from flask_restful import Resource, reqparse
from endpoints import Auxiliary
from database import DbConnection


# unused -- supports requirement G32
class Unpublish(Resource):
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        """"Removes the specified.study from search results.

        This operation will fail if the user making the request is not the author of the study.
        An unpublished study can still be accessed via other user's historical lists,
        and the template can still be accessed via /deliver.

        Args:
            user_id (String): The identifier for the user trying to unpublish the study.
            study_id (Integer): The identifier of the study the user is trying to unpublish.

        Returns:
            JSON: {"Success": True} if unpublished, {"Success": False} if no such study authored by user.
        """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("study_id", type=int, required=True, help="The study ID to be unpublished is an integer.")
        returned_args = parser.parse_args()
        user_id = kwargs["user_id"]
        study_id = returned_args.get("study_id", None)

        connect = DbConnection.connector()["Studies"]
        study = connect.find_one_and_update({"Study_id": study_id, "Author_id": user_id},
                                            {"$currentDate": {"Denied": {"$type": "timestamp"}}})
        result = study is not None
        # return converted output
        return jsonify({"Success": result})
