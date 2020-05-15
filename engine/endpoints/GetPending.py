from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from database import DbConnection
from studystore.FindingFiveStudyStoreUser import FindingFiveStudyStoreUser as f5user
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy as f5study
from endpoints import Auxiliary


class GetPending(Resource):
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        """"Provides a list of pending studies from the database.

            Provides a list of studies, in JSON format, that have been neither approved nor denied.
            Excludes studies authored by the accessing user.
            If limit is given, no more than limit studies will be returned.

            Args:
                token (String): A tokenized identifier of a user, tokenization is done with
                                a flask GET HTTP request using the crypto blueprint and formatted like this.
                                ('/token/generate', data={'user_id': 'VALID_USER_IN_DATABASE'})
                                
                limit (Integer): The maximum number of studies to return. Defaults to unlimited when missing or negative.


            Returns:
                JSON: The list of pending studies.
            """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("limit", type=int, default=-1)

        # the second parameter to each method call is purely for consistency,
        # they don't actually do anything. They should match the defaults above.
        returned_args = parser.parse_args()
        limit = returned_args.get("limit", -1)
        user_id = kwargs["user_id"]

        # build search parameters
        params = {"Author_id": {"$ne": user_id}, "Approved": {"$exists": False}, "Denied": {"$exists": False}}

        # query database
        studyList = Auxiliary.getStudies(params, limit)
        # convert output
        out = Auxiliary.studyListToDictList(studyList)
        # return converted output
        return jsonify(out)
