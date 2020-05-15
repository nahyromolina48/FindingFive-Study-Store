from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from database import DbConnection
from studystore.FindingFiveStudyStoreUser import FindingFiveStudyStoreUser as f5user
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy as f5study
from endpoints import Auxiliary


class GetAdminDetails(Resource):
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        """"Provides the full details for a study from the database.

            Provides a study, in JSON format, with all fields of data, given the ID of the study.
            Intended for use in administrative review.
            For normal previewing, use GetPreview.get().

            Args:
                study_id (Integer): The identifier of the study to be reviewed.


            Returns:
                JSON: The study with its template.
            """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("study_id", type=int, required=True, help="Specify a study for details.")

        # the second parameter to each method call is purely for consistency,
        # they don't actually do anything. They should match the defaults above.
        returned_args = parser.parse_args()
        study_id = returned_args.get("study_id", None)

        # query database
        study = Auxiliary.getStudy(study_id)

        # return converted output
        return jsonify(study.build_dict())
