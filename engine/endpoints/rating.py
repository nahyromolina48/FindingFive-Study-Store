from database import DbConnection


def ratingsys(id, user, name, rate, comment):
    """Creates a review for a study and updates that study's rating.
    If the user is submitting a duplicate review (same study), the previous review will be overwritten.

    Args:
         id (Integer): The identifier for the study being reviewed.
         user (String): The identifier for the user making the review.
         name (String): The name of the user, as it should be displayed on the review.
         rate (Integer): The rating the user is applying to the study.
         comment (String): The comment the user has about the study.

    Returns:
        Nothing.
    """
    connect = DbConnection.connector()
    review = connect["Reviews"]
    # post the review, overwriting any existing review
    review.update_one({"Study_id": id, "User_id": user},
                      {"$set": {"Study_id": id, "User_id": user, "Name": name, "Rating": rate, "Comment": comment}},
                      upsert=True)
    update_study_rating(id)

def remove_rating(study_id, user_id):
    """Removes a review for a study and updates that study's rating.

    Args:
        study_id (Integer): The study that was reviewed.
        user_id (String): The user whose review should be removed.

    Returns:
        Boolean: True if a study was deleted."""
    connect = DbConnection.connector()
    review = connect["Reviews"]
    # delete the review
    result = review.delete_one({"Study_id": study_id, "User_id": user_id})
    update_study_rating(study_id)
    return result.deleted_count > 0


def update_study_rating(id):
    """Updates a study's rating based on the reviews in the database.

    Intended for use after a review has been made or removed.

    Args:
        id (Integer): The identifier of the study to update.

    Returns:
        Integer: The new value of teh rating.
    """
    # find the new overall rating
    connect = DbConnection.connector()
    review = connect["Reviews"]
    query = review.find({"Study_id": id})
    ratelist = []
    for rates in query:
        ratelist.append(rates["Rating"])
    if (len(ratelist) == 0):
        average = 0
    else:
        average = sum(ratelist) / len(ratelist)  # Gets the average rating of this study
        average = round(average)  # this average is then converted to a whole number

    # update the rating for the study itself
    rater = connect["Studies"]
    rater.update_one({"Study_id": id}, {"$set": {"Rating": average}})
    return average


def getReviews(study_id):
    """Returns all the reviews for a given study.

    Each review is limited to the name, occupation, rating, and comment.

    Args:
        study_id (Integer): The identifier of the study for which to return reviews.

    Returns:
        List<Dict>: A list of dictionaries containing the name, occupation, rating, and comment for each review.
    """
    # query the database
    connect = DbConnection.connector()["Reviews"]
    queryresults = connect.find({"Study_id": study_id,
                                 "Name": {"$exists": True},
                                 "Rating": {"$exists": True},
                                 "Comment": {"$exists": True}})
    # convert tot he output format
    reviewlist = []
    for review in queryresults[:]:
        outdoc = dict()
        outdoc["name"] = review["Name"]
        outdoc["rating"] = review["Rating"]
        outdoc["comment"] = review["Comment"]
        reviewlist += [outdoc]
    return reviewlist
