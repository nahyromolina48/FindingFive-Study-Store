from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from database import DbConnection
from studystore.FindingFiveStudyStoreUser import FindingFiveStudyStoreUser as f5user
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy as f5study
from endpoints import Auxiliary
import re


class Search(Resource):
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        """"Provides a list of studies from the database.

            Provides a list of studies, in JSON format, that meet some specified requirements.
            All parameters are optional, except for the token required for authentication.
            Providing none of the optional parameters will result in all studies being returned,
            but may result in a connection time out.
            If title is given, return only studies with that title.
            If keywords are given, return only studies with all of those keywords.
            If keyword_all is false, each study need only have one or more keywords, not necessarily all of them.
            If searchInput is given, return studies with that title OR any keyword in searchInput,
            splitting by a comma with an optional space after it.
            Specifying title or keywords with searchInput will require each individual parameter to be satisfied.
            If limit is given, no more than limit studies will be returned.
            If price_min is given, return only studies at that price or higher.
            If price_max is given, return only studies at that price or lower.
            If price_min is greater than price_max, ignore price_max.
            For the purposes of this method, the price of a study may not be negative,
            so all negative values of price_min and price_max will be ignored.
            If duration_min is given, return only studies at that duration or higher.
            If duration_max is given, return only studies at that duration or lower.
            If duration_min is greater than duration_max, ignore duration_max.
            For the purposes of this method, the duration of a study may not be negative,
            so all negative values of duration_min and duration_max will be ignored.
            If rating_min is given, return only studies with that rating or higher.
            If rating_max is given, return only studies with that rating or lower.
            If rating_min is greater than or equal to rating_max, ignore rating_max.
            The valid options for rating_min and rating_max are 0, 1, 2, 3, 4, and 5.
            If category is given, return only studies with that category.
            If sub_category is given, return only studies with that sub category.
            If institution is given, return only studies with that institution.
            If max_days_since_upload is given, return only studies that have been uploaded within that number of days.

            Args:
                title (String): The title that a study must have..
                keywords (List<String>): Contains all the keywords that a study must have.
                keyword_all (Boolean): If false, any non-empty subset of the keywords is sufficient to match.
                searchInput (String): The title or comma-seperated keyword set that a study must have at least one of.
                limit (Integer): The maximum number of studies to return. Defaults to unlimited when missing or negative.
                price_min (Integer): The minimum price, in credits, that a study may have.
                price_max (Integer): The maximum price, in credits, that a study may have.
                duration_min (Integer): The minimum duration, in minutes, that a study may have.
                duration_max (Integer): The maximum duration, in minutes, that a study may have.
                rating_min (Integer): The minimum rating that a study may have. Must be in the range [0, 5].
                rating_max (Integer): The maximum rating that a study may have. Must be in the range [0, 5].
                category (String): The category that a study must have.
                sub_category (String): The sub category that a study must have.
                institution (String): The institution that a study must have.
                max_days_since_upload (Integer): The maximum days after upload that a study may be.


            Returns:
                JSON: The list of studies that meet the specified requirements.
            """
        # obtain parameters
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("title", type=str)
        parser.add_argument("keywords", type=str, action="append")
        parser.add_argument("keyword_all", type=inputs.boolean, default=True)
        parser.add_argument("searchInput", type=str)
        parser.add_argument("limit", type=int, default=-1)
        parser.add_argument("price_min", type=int, default=0)
        parser.add_argument("price_max", type=int, default=-1)
        parser.add_argument("duration_min", type=int, default=0)
        parser.add_argument("duration_max", type=int, default=-1)
        parser.add_argument("rating_min", type=int, default=0, choices=(0, 1, 2, 3, 4, 5))
        parser.add_argument("rating_max", type=int, default=5, choices=(0, 1, 2, 3, 4, 5))
        parser.add_argument("category", type=str)
        parser.add_argument("sub_category", type=str)
        parser.add_argument("institution", type=str)
        parser.add_argument("max_days_since_upload", type=int)

        # the second parameter to each method call is purely for consistency,
        # they don't actually do anything. They should match the defaults above.
        returned_args = parser.parse_args()
        title = returned_args.get("title", None)
        keywords = returned_args.get("keywords", None)
        keyword_all = returned_args.get("keyword_all", True)
        searchInput = returned_args.get("searchInput", None)
        limit = returned_args.get("limit", -1)
        price_min = returned_args.get("price_min", 0)
        price_max = returned_args.get("price_max", -1)
        duration_min = returned_args.get("duration_min", 0)
        duration_max = returned_args.get("duration_max", -1)
        rating_min = returned_args.get("rating_min", 0)
        rating_max = returned_args.get("rating_max", 5)
        category = returned_args.get("category", None)
        sub_category = returned_args.get("sub_category", None)
        institution = returned_args.get("institution", None)
        max_days_since_upload = returned_args.get("max_days_since_upload", None)

        # build search parameters
        params = {"Approved": {"$exists": True}, "Denied": {"$exists": False}}
        if title is not None:
            params["Title"] = title
        if keywords is not None:
            # intersection/and
            if keyword_all is True:
                params["Keywords"] = {"$all": keywords}
            # union/or
            else:
                params["Keywords"] = {"$in": keywords}
        if searchInput is not None:
            splitSearch = re.split(r', ?', searchInput)
            params["$or"] = [{"Title": searchInput}, {"Keywords": {"$in": splitSearch}}]
        self.addRange(params, price_min, price_max, "CostinCredits")
        self.addRange(params, duration_min, duration_max, "Duration")
        self.addRange(params, rating_min, rating_max, "Rating")
        if category is not None:
            # using $in so that we can make Categories an array or string without breaking this code
            params["Categories"] = {"$in": [category]}
        if sub_category is not None:
            # using $in so that we can make Sub_Categories an array or string without breaking this code
            params["Sub_Categories"] = {"$in": [sub_category]}
        if institution is not None:
            params["Institution"] = institution
        if max_days_since_upload is not None:
            max_millis = max_days_since_upload * 86400000  #24 * 60 * 60 * 1000
            params["$expr"] = {"$lt": [{"$subtract": ["$$NOW", "$Timestamp"]}, max_millis]}
        # query database
        studyList = Auxiliary.getStudies(params, limit)
        # convert output
        out = Auxiliary.studyListToDictList(studyList)
        for d in out:
            d["reviews"] = []
        # return converted output
        return jsonify(out)

    def addRange(self, param_dict, min, max, field_name):
        """"Adds a range for a field to a filter.

            The range is assumed to be inclusive.
            If max is less than min, max is ignored.
            Negative values of min and max are also ignored.
            If max and min are the same but neither has been ignored,
            the range simplifies to that same number.
            This function in theory accepts doubles,
            but was designed for integers.

            Args:
                param_dict (Dict): The filter to which the range is to be added, passed by reference.
                min (Integer): The minimum value in the range.
                max (Integer): The maximum value in the range.
                field_name (String): The field that is to be limited to the specified range.


            Returns:
                None.
            """
        # equivalent to default, so don't add anything
        if min <= 0 and max < 0:
            pass
        # min is given but max is ignored
        # (max < 0 is subsumed by max < min in this case)
        elif min > 0 and max < min:
            param_dict[field_name] = {"$gte": min}
        # the above two cases handle all values of min combined with a negative value of max,
        # so max must be greater than or equal to zero past this point.

        # when equal, we can just look for that value
        elif min == max:
            param_dict[field_name] = min
        # we know max >= 0 from the cases above, so we only need to check if min is ignored
        elif min < 0:
            param_dict[field_name] = {"$lte": max}
        # we know both min and max are relevant and min < max
        else:
            # using implicit $and operation
            param_dict[field_name] = {"$gte": min, "$lte": max}

