import base64
import binascii
import hashlib as hl
import os

import nacl.exceptions
from dotenv import load_dotenv
from nacl import secret, utils


class TokenService():
    """Handles Session Token Operations
    Verifies the token passed by the user is Valid.
    """

    def __init__(self):
        self.secret_key = self.load_secret_key()

    def load_secret_key(self):
        """Loads the Private key from disk.
        Reads the private key from the .env file. If the file doesn't exist,
        Creates a new private key.

        Args:
            None

        Returns:
           bytes:The Secret Key to be used in the Box
        """
        env_path = os.path.abspath(os.path.dirname(__file__))
        print(env_path)
        location = os.path.join(env_path, 'secrets')
        load_dotenv(dotenv_path=location)
        secret_key = os.getenv('SECRET')
        if secret_key is None:
            server_key = self.create_keys(location)
            return server_key
        return base64.decodebytes(secret_key.encode('ascii'))

    def decode_base64(self, client_resp):
        """Decodes the client response from Base64.
        Takes the encrypted client response and decodes from Base64.


        Args:
            client_resp(dict):The dict from the client's response

        Returns:
            dict
        """
        client_respz = client_resp.copy()
        client_respz["user_id"] = base64.decodebytes(client_resp["user_id"].encode('ascii'))
        client_respz["user_type"] = base64.decodebytes(client_resp["user_type"].encode('ascii'))
        client_respz["credits"] = base64.decodebytes(client_resp["credits"].encode('ascii'))
        client_respz["nonce"] = base64.decodebytes(client_resp["nonce"].encode('ascii'))
        return client_respz

    def decrypt(self, client_resp):
        ''' Decrypt the client's response.
        Decrypt the client's response dict in order to verify the client
        Has access to the website.

        Args:
            client_resp(dict):The dict from the client's response

        Returns:
            dict: Returns decrypted results otherwise returns False

        Raises:
            nacl.exceptions.CryptoError: The box failed to decrypt a field.
        '''
        box = secret.SecretBox(self.secret_key)
        decrypted = dict()
        print(client_resp["user_id"])
        print(client_resp['nonce'])
        try:
            client_resp['user_id'] = client_resp['user_id'] + b'd'
            decrypted["user_id"] = box.decrypt(client_resp['user_id']).decode('utf-8')
            decrypted["user_type"] = (int.from_bytes(box.decrypt(client_resp["user_type"]), byteorder="little"))
            decrypted["credits"] = (int.from_bytes(box.decrypt(client_resp["credits"]), byteorder="little"))
        except nacl.exceptions.CryptoError:
            # message wasn't crafted correctly
            return False
        else:
            return decrypted

    # print(box.decrypt())

    def verify_msg(self, client_resp):
        """Check the authenticy of the user provided values.
        This is the main function of the class to determine if the given response
        Args:
            self: Refernce to the given class
            client_resp: The dict of values passed by the client

        Returns:
            bool,dict : Returns the status of decrpytion and the associated dict.

        """
        client_resp = self.decode_base64(client_resp)
        print(client_resp)
        user_id = client_resp['user_id']
        user_type = client_resp["user_type"]
        credits = client_resp["credits"]
        user_hash = client_resp["hash"]
        hashy = hl.sha256()
        user_hex_vals = binascii.hexlify(user_id + user_type + credits)
        hashy.update(user_hex_vals)
        decrypt = self.decrypt(client_resp)
        if decrypt is False:
            return False, None

        if hashy.hexdigest() == user_hash:
            return True, decrypt
        return False, None

    def create_keys(self, location):
        ''' Create  Symmetric Private Key
        This creates and writes to the .env the private key used in the creation
        and verification of client tokens.
        Args:
            location(str): Where the file to be written is located on the device.

        Returns:
            bytes: The newly created private key.
        '''
        # create the server key  and stores in a local file.
        server_key = utils.random(secret.SecretBox.KEY_SIZE)
        with open(location, "a") as f:
            f.write("SECRET=")
            f.write(base64.encodebytes(server_key).decode('ascii'))
        return server_key
