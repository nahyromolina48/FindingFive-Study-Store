import binascii
import hashlib as hl

class UserToken():
    def __init__(self):
        #might not be needed
        self.user_id='kazookid'
        self.secrek_key=47969418713
        self.user_type= 2
        self.credits_avail=20
        self.user_token = None


    def create_token(self):
        string_token = str(self.user_id+str(self.secrek_key)+str(self.user_type)+str(self.credits_avail))
        token_hex = binascii.hexlify(string_token.encode("utf-8"))
        hash_f = hl.sha256()
        hash_f.update(token_hex)
        return hash_f.hexdigest()

    def check_hash(self,user_provided):
        back_end_token=self.create_token()
        if back_end_token == user_provided:
            return 200
        return 400

    def read_token(self,token_hex):
        token_hex_byte=token_hex["token"]
        result =self.check_hash(token_hex_byte)
        if result ==200:
            token_unhex = binascii.unhexlify(token_hex)
            #this is the user provided hash
            token= token_unhex.decode("utf-8")
            if str(self.secrek_key) not in token:
                return 400, "Token not found"
            return self.create_user_json(token)
        return result

    def create_user_json(self,decoded_token):
        tokens=decoded_token.split(str(self.secrek_key))
        user_repr = dict()
        user_repr["user_id"]= tokens[0]
        user_repr["user_type"] = tokens[1][0]
        user_repr["credits"] = tokens[1][1:]
        return user_repr
    #def read_secret_from_disc(self):

if __name__ == '__main__':
    user_t=UserToken()
    gen_token=user_t.create_token()
    print(user_t.read_token(gen_token))
