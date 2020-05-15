import functools, time
from flask import abort, jsonify
from flask_restful import reqparse
from crypto.GuiToken import Generator
from database import DbConnection
from studystore.FindingFiveStudyStoreUser import FindingFiveStudyStoreUser as f5user
from studystore.FindingFiveStudyStoreStudy import FindingFiveStudyStoreStudy as f5study
from suggestions.study_cache import StudyCache
from typing import Union


def getStudy(study_id):
    """Grabs a study given its ID.

    Pulls from the database and returns a FindingFiveStudyStoreStudy object.

    Args:
        study_id (int): The ID assigned to a study at upload.

    Returns:
        FindingFiveStudyStoreStudy: The associated study in the database.
    """
    connect = DbConnection.connector()["Studies"]
    study = {"Study_id": study_id}
    seek = connect.find_one(study)

    return f5study(study_id, seek["Title"], seek["Author"], seek["CostinCredits"], seek["Purpose"],
                   seek["References"],
                   seek["Categories"], seek["Sub_Categories"], seek["Keywords"], seek["Num_Stimuli"],
                   seek["Num_Responses"], seek["Randomize"], seek["Duration"], seek["Num_trials"], seek["Rating"],
                   seek["Institution"], seek["Template"], seek["Images"], seek["Abstract"], seek["Author_id"],
                   seek["Upload Date"])


def getTitle(study_id):
    """Grabs a study's title given the study's ID.

    Returns None if the study does not exist, allowing this method to be used to check existence.

    Args:
        study_id (int): The ID assigned to a study at upload.

    Returns:
        String: The associated study's title field from the database, or None when no such study exists.
    """
    connect = DbConnection.connector()["Studies"]
    study = {"Study_id": study_id}
    seek = connect.find_one(study, ["Title"])
    if seek is None:
        return None
    else:
        return seek["Title"]


def getTemplate(study_id):
    """Grabs a study's template given the study's ID.

    Pulls from the database and returns a String object representing the JSON template.

    Args:
        study_id (int): The ID assigned to a study at upload.

    Returns:
        String: The associated study's template field from the database.
    """

    connect = DbConnection.connector()["Studies"]
    study = {"Study_id": study_id}
    seek = connect.find_one(study, ["Template"])
    return seek["Template"]


def getStudies(params, maxStudies=-1):
    """Grabs a list of studies given some parameters they need to meet.

    Pulls from the database and returns a list of FindingFiveStudyStoreStudy objects.
    Each object will have the fields given in params equal to the values paired with them in params.

    Args:
        params (dict): Pairs field names with the values they must have.
        maxStudies (int): If greater than or equal to zero, no more than max studies will be in the output list.

    Returns:
        list<FindingFiveStudyStoreStudy>: The first "max" studies that have the given params.
    """

    # if asked for zero studies, just return
    if (maxStudies == 0):
        return []
    # change to the number the Mongo code likes uses for no limit
    elif (maxStudies < 0):
        maxStudies = 0

    # acquire studies
    connect = DbConnection.connector()["Studies"]
    seek = connect.find(filter=params, projection={"Template": False, "Images": False}, limit=maxStudies, collation={'locale':'en_US', 'strength':1})

    # get the number of studies returned - params maintains the filter
    numStudies = seek.collection.count_documents(params, collation={'locale':'en_US', 'strength':1})

    # make sure we don't return more studies than expected
    numWanted = min(numStudies, maxStudies)
    if maxStudies == 0:
        numWanted = numStudies

    studyList = []
    # not sure if this actually returns a list
    for study in seek[0:numWanted]:
        studyList.append(
            f5study(study["Study_id"], study["Title"], study["Author"], study["CostinCredits"], study["Purpose"],
                    study["References"],
                    study["Categories"], study["Sub_Categories"], study["Keywords"], study["Num_Stimuli"],
                    study["Num_Responses"], study["Randomize"], study["Duration"], study["Num_trials"], study["Rating"],
                    study["Institution"], "Template redacted", [], study["Abstract"], study["Author_id"],
                    study["Upload Date"]))
    return studyList


def studyListToDictList(study_list):
    """Converts the output from GetStudies to jsonify-ready form.

    Args:
        study_list (List<FindingFiveStudyStoreStudy>): A list of study objects to convert.


    Returns:
        List<Dict>: A list of dictionaries containing the fields from the studies given.
    """
    # code adapted from gui_endpoints/preview_study
    built_json = list()
    for study in study_list:
        built_json.append(study.build_dict())
    return built_json


def createUser(user):
    """Creates a new user in the database.

    If the user already exists, do nothing.
    A user object can be created with just a user ID.

    Args:
        user (FindingFiveStudyStoreUser): The user object to store.

    Returns:
        Boolean: True if the user was created, False if they user was already present."""

    connect = DbConnection.connector()["Users"]
    filter = {"User_id": user.get_userId()}
    update = {"$setOnInsert": user.build_database_doc()}
    # this should be returning the "pre-update" doc, which will be None if nothing matches the filter.
    result = connect.find_one_and_update(filter, update, upsert=True)
    return result is None


def getUser(user_id):
    """Grabs a user given its ID.

    Pulls from the database and returns a FindingFiveStudyStoreUser object.

    Args:
        user_id (String): The ID associated with a user at authentication.

    Returns:
        FindingFiveStudyStoreUser: The associated user in the database.
    """

    connect = DbConnection.connector()["Users"]
    user = {"User_id": user_id}
    seek = connect.find_one(user)
    if seek is not None:
        return f5user(user_id, seek["Num Credits"], seek["Owned Studies"], seek["Viewed Studies"], seek["Wish List"], seek["Author List"])
    else:
        return f5user(user_id)


def updateUser(user):
    """"Updates a user in the database.	
    Pushes a new version of the user data into the database. Assumes the current ID already exists.	
    Args:	
        user (FindingFiveStudyStoreUser): The new data to write to the database.	
    Returns:	
        Nothing.	
    """

    connect = DbConnection.connector()["Users"]
    userJ = {"User_id": user.get_userId()}
    changes = {"$set": {"Num Credits": user.get_numCredits(),
                        "Owned Studies": user.get_ownedStudies(),
                        "Viewed Studies": user.get_viewedStudies(),
                        "Wish List": user.get_wishList(),
                        "Author List": user.get_authorList()}}
    connect.update_one(userJ, changes)


def addOwned(user_id, study_id, cost):
    """Decreases a user's credits to purchase a study.

    Atomically decreases a user's credits and adds the study to the user's list of owned studies.
    Does not verify that the referenced study actually exists.
    If the study is already in the list, a duplicate will not be created.

    Args:
        user_id (String): The ID of the user purchasing the study.
        study_id (Integer): The ID of the study being purchased.
        cost (Integer): The positive number of credits to deduct from the user for the study.

    Returns:
        Nothing.
    """

    connect = DbConnection.connector()["Users"]
    user = {"User_id": user_id}
    changes = {"$inc": {"Num Credits": 0 - cost},
               "$addToSet": {"Owned Studies": study_id}}
    connect.update_one(user, changes)


def addAuthored(user_id, study_id):
    """Marks a user as being the author of a study.

    Also marks the user as being an owner of that study.
    Does not change the study itself.
    Intended for use with /upload.

    Args:
        user_id (String): The ID of the user authoring the study.
        study_id (Integer): The ID of the study being uploaded.

    Returns:
        Nothing."""

    connect = DbConnection.connector()["Users"]
    user = {"User_id": user_id}
    changes = {"$addToSet": {"Owned Studies": study_id, "Author List": study_id}}
    connect.update_one(user, changes)


def isOwned(user_id, study_id):
    """"Returns the ownership status of the study.

    Returns true only if the indicated user owns the indicated study,
    otherwise returns false.

    Args:
        user_id (String): The identifier for the user who may own the study.
        study_id (int): The identifier for the study the user may own.

    Returns:
        boolean: True if the user owns the study, else false.
    """

    connect = DbConnection.connector()["Users"]
    user = {"User_id": user_id,
            "Owned Studies": {"$in": [study_id]}}
    # if such a user exists, we get the user, else we get None
    return connect.find_one(user) != None


def isWishlisted(user_id, study_id):
    """"Returns the wish list status of the study.

    Returns true only if the indicated user wishes for the indicated study,
    otherwise returns false.

    Args:
        user_id (String): The identifier for the user who may wish for the study.
        study_id (int): The identifier for the study the user may wish for.

    Returns:
        boolean: True if the user wishes for the study, else false.
    """

    connect = DbConnection.connector()["Users"]
    user = {"User_id": user_id,
            "Wish List": {"$in": [study_id]}}
    # if such a user exists, we get the user, else we get None
    return connect.find_one(user) != None


def addViewed(user_id, study_id):
    """"Adds a study to a user's list of viewed studies.

    Adds the study to the end of the list, even if viewed before.

    Args:
        user_id (String): The ID of the user viewing the study.
        study_id (int): The ID of the study being viewed.

    Returns:
        Nothing.
    """

    connect = DbConnection.connector()["Users"]
    user = {"User_id": user_id}
    lister = {"$push": {"Viewed Studies": study_id}}
    connect.update_one(user, lister)


def addWishlist(user_id, study_id):
    """"Adds a study to a user's wish list of studies.

    Adds the study to the end of the list, unless already in the wish list.

    Args:
        user_id (String): The ID of the user wish listing the study.
        study_id (int): The ID of the study being saved to the wish list.

    Returns:
        Nothing.
    """

    connect = DbConnection.connector()["Users"]
    user = {"User_id": user_id}
    lister = {"$addToSet": {"Wish List": study_id}}
    connect.update_one(user, lister)


def removeWishlist(user_id, study_id):
    """Removes a study from a user's wish list of studies.

    Removes all occurences in the list.

    Args:
        user_id (String): The ID of the user removing the study from the wish list.
        study_id (int): The ID of the study being removed from the wish list.

    Returns:
        Nothing.
    """

    connect = DbConnection.connector()["Users"]
    user = {"User_id": user_id}
    lister = {"$pull": {"Wish List": study_id}}
    connect.update_one(user, lister)


def addNotification(user_id, title, body, type):
    """"Posts a notification to the database.

    Posts the notification, along with an additional timestamp, to the database.

    Args:
        user_id (String): The user who should receive the notification.
        title (String): The header of the notification.
        body (String): The main portion of the notification for when the user clicks on it.
        type (String): The type of notifaction, such as approval, denial, or welcome.

    Returns:
        Nothing.
    """
    connect = DbConnection.connector()["Notifications"]
    notification = {"User_id": user_id, "Title": title, "Body": body, "Type": type}
    connect.insert(notification)
    timeUpdate = {"$currentDate": {"Timestamp": True}}
    notificationFinder = notification
    notificationFinder["Timestamp"] = {"$exists": False}
    connect.update_one(notificationFinder, timeUpdate, upsert=True)


def timestampAndGetAuthor(study_id, field_name):
    """"Adds a timestamp to a study and returns the author ID of that study.

    Timestamps a study, using  field_name as the name of the timestamp.
    Returns the author ID of the study.
    These two actions are combined for optimization of the administrative review endpoint ReviewPending.

    Args:
        study_id (Integer): The identifier of the study to timestamp.
        field_name (String): The name to attach to the timestamp.


    Returns:
        String: The author ID of the specified study.
    """
    connect = DbConnection.connector()["Studies"]
    study = connect.find_one_and_update({"Study_id": study_id},
                                        {"$currentDate": {field_name: {"$type": "timestamp"}}},
                                        ["Author_id"])
    return study["Author_id"]


def auth_dec(func):
    '''Checks for the existence of a JWT token in the url.

    This method will check and verify if the given token was
    generated by FindingFive.It will pass the user id to the given
    function.

    Args
     func: The function passed to the decorator.
    Returns:
        Function: The function passed to the decorator with the user id included.
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("token", type=str, required=True, location='headers', help="The JWT token")
        returned_args = parser.parse_args()
        gen = Generator()
        resp = gen.authenticate_token(returned_args['token'])
        if type(resp) is dict:
            abort(401, description=resp['msg'])
        kwargs["user_id"] = resp
        value = func(*args, **kwargs)
        return value

    return wrapper


def time_backend(func):
    '''Calculates the amount of time to execute the given function.
    
    Args
        func (Function): The function passed to the decorator. s
    Returns:
        Json : The difference between the end and start time.
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()
        return jsonify({"time": end - start})
