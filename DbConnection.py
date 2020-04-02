from pymongo import MongoClient
import ssl
import os
from dotenv import load_dotenv


# This should be used to connect to the database remotely
# username and password should be called externally
# Variable references:
# info --Dict object
# tb -- String Object
# curr -- Dict Object
# new_data -- Dict Object

# connects to the mongo atlas
def connector():
    env_path = os.path.abspath(os.path.dirname(__file__))
    location = os.path.join(env_path, '.env')
    load_dotenv(dotenv_path=location)
    client = MongoClient(
        "mongodb+srv://Engine:qhcFrP65n8joJvso@cluster0-v76zg.mongodb.net/test?retryWrites=true&w=majority", ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE)  # MongoClient(os.getenv('MongoURL'))
    db = client["StudyStore"]
    return db
