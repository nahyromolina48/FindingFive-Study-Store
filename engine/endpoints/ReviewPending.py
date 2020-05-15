from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from database import DbConnection
from studystore.FindingFiveStudyStoreUser import FindingFiveStudyStoreUser as f5user
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy as f5study
from endpoints import Auxiliary


class ReviewPending(Resource):
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        """"Reviews a pending study.

            Approves or denies a given study.
            Creates a notification to alert the user, based on the parameters.
            If an optional parameter is not given, that field is assumed to be acceptable.
            Fails, modifying nothing, if the user is the author of the study.

            Args:
                user_id (String): The identifier of the user approving or denying the study, required.
                study_id (Integer): The identifier of the study being reviewed, required.
                approved (Boolean): Whether to approve or deny this study. When true, ignore all following paramaters.
                title (String): The comment on what was wrong with the title.
                reference (String): The comment on what was wrong with the references.
                purpose (String): The comment on what was wrong with the purpose.
                categories (String): The comment on what was wrong with the categories.
                subcategories (String): The comment on what was wrong with the subcategories.
                keywords (String): The comment on what was wrong with the keywords.
                abstract (String): The comment on what was wrong with the abstract.
                num_stimuli (String): The comment on what was wrong with the number of stimuli.
                duration (String): The comment on what was wrong with the duration of the study.
                num_responses (String): The comment on what was wrong with the number of responses.
                num_trials (String): The comment on what was wrong with the number of trials.
                randomized (String): The comment on what was wrong with the randomization of the study.
                images (String): The comment on what was wrong with the images.
                template (String): The comment on what was wrong with the JSON template.


            Returns:
                JSON: {"Success":True} unless the review failed.
            """
        # establish parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("study_id", type=int, required=True)
        parser.add_argument("approved", type=inputs.boolean, default=False)
        parser.add_argument("title", type=str)
        parser.add_argument("reference", type=str)
        parser.add_argument("purpose", type=str)
        parser.add_argument("categories", type=str)
        parser.add_argument("subcategories", type=str)
        parser.add_argument("keywords", type=str)
        parser.add_argument("abstract", type=str)
        parser.add_argument("num_stimuli", type=str)
        parser.add_argument("duration", type=str)
        parser.add_argument("num_responses", type=str)
        parser.add_argument("num_trials", type=str)
        parser.add_argument("randomized", type=str)
        parser.add_argument("images", type=str)
        parser.add_argument("template", type=str)

        # obtain first parameters
        returned_args = parser.parse_args()
        study_id = returned_args.get("study_id", -1)
        user_id = kwargs["user_id"]
        approved = returned_args.get("approved", None)

        # check for author
        user = Auxiliary.getUser(user_id)
        if study_id in user.get_authorList():
            return jsonify({"Success": False, "Reason": "User is Author."})

        # check for non-existent study, storing the title for later
        study_title = Auxiliary.getTitle(study_id)
        if study_title is None:
            return jsonify({"Success": False, "Reason": "No such study."})

        # check for approval
        if approved is True:
            user_id = Auxiliary.timestampAndGetAuthor(study_id, "Approved")
            body = "Your study, " + study_title + ", was approved and is now visible in the Study Store."
            Auxiliary.addNotification(user_id, "Study approved.", body, "Approval")
            return jsonify({"Success": True})

        # otherwise we need all the other parameters
        title = returned_args.get("title", None)
        reference = returned_args.get("reference", None)
        purpose = returned_args.get("purpose", None)
        categories = returned_args.get("categories", None)
        subcategories = returned_args.get("subcategories", None)
        keywords = returned_args.get("keywords", None)
        abstract = returned_args.get("abstract", None)
        num_stimuli = returned_args.get("num_stimuli", None)
        duration = returned_args.get("duration", None)
        num_responses = returned_args.get("num_responses", None)
        num_trials = returned_args.get("num_trials", None)
        randomized = returned_args.get("randomized", None)
        images = returned_args.get("images", None)
        template = returned_args.get("template", None)

        # build response body
        body_string = "Your study, " + study_title + ", has been denied."
        body_string += "Problems with the title: " + str(title) +"\n"
        body_string += "Problems with the reference: " + str(reference) + "\n"
        body_string += "Problems with the purpose: " + str(purpose) + "\n"
        body_string += "Problems with the categories: " + str(categories) + "\n"
        body_string += "Problems with the subcategories: " + str(subcategories) + "\n"
        body_string += "Problems with the keywords: " + str(keywords) + "\n"
        body_string += "Problems with the abstract: " + str(abstract) + "\n"
        body_string += "Problems with the number of stimuli: " + str(num_stimuli) + "\n"
        body_string += "Problems with the duration of the study: " + str(duration) + "\n"
        body_string += "Problems with the number of responses: " + str(num_responses) + "\n"
        body_string += "Problems with the number of trials: " + str(num_trials) + "\n"
        body_string += "Problems with the randomization: " + str(randomized) + "\n"
        body_string += "Problems with the images: " + str(images) + "\n"
        body_string += "Problems with the template: " + str(template) + "\n"

        # mark the study and post the notification
        user_id = Auxiliary.timestampAndGetAuthor(study_id, "Denied")
        Auxiliary.addNotification(user_id, "Study denied.", body_string, "Denial")
        return jsonify({"Success": True})
