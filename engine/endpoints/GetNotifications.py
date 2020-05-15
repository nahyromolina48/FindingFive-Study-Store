from flask import jsonify
from flask_restful import Resource, reqparse
from endpoints import Auxiliary
from database import DbConnection

class GetNotifications(Resource):
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        """"Returns the list of .notifications sent to a user.

        Returns all notifications sent to a user, starting with the newest.

        Args:
            token (String): A tokenized identifier of a user, tokenization is done with
                            a flask GET HTTP request using the crypto blueprint and formatted like this.
                            ('/token/generate', data={'user_id': 'VALID_USER_IN_DATABASE'})

        Returns:
            JSON: The list of notifications.
        """
        user_id = kwargs["user_id"]
        notifications = getMessages(user_id)
        # return converted output
        return jsonify(notifications)

def getMessages(user_id):
    """"Returns the list of .notifications sent to a user.

    Returns all notifications sent to a user, starting with the newest.

    Args:
        user_id (String): The identifier for the user for whom the notifications are to be returned.

    Returns:
        JSON: The list of notifications.
    """
    # acquire notifications
    connect = DbConnection.connector()["Notifications"]
    seek = connect.find(filter={"User_id": user_id}, sort=[('Timestamp', -1)])
    # build list
    out = []
    for notif in seek:
        out.append({"title": notif["Title"],
                    "body": notif["Body"],
                    "type": notif["Type"],
                    "timestamp": notif["Timestamp"]})
    return out
