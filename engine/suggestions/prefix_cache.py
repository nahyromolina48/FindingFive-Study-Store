import redis
import uuid


class SearchCache():
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.max_set_size = 400

    def check_existence(self, title):
        result = self.r.exists(title)
        if result == 1:
            return True
        return False

    def add_new_word(self, full):
        given_words = full.lower().split(" ")
        sent_hash = self.get_hash_id(full)
        self.r.hset(sent_hash, "title", full)
        pipe = self.r.pipeline()
        for word in given_words:
            if not self.check_existence(word):
                # now iterate over all of the partial strings and use the partial string to map to a sorted set.
                # each sorted set will continain the id:score so it can sort the entries.
                try:
                    for partial in self.generate_prefix(word):

                        set_id = self.get_set_id(partial)
                        status, set_size = self.check_set_size(set_id)
                        if status:

                            pipe.zadd(set_id, {sent_hash: 1.0})
                        else:
                            self.remove_prefix(set_id, sent_hash)
                except redis.exceptions.ResponseError as e:
                    print(e.args)
        pipe.execute()

    def generate_prefix(self, word):
        for index, char in enumerate(word):
            index = index + 1
            if index == len(word):
                # this may be old.
                yield word[0:index] + '*'
            yield word[0:index]

    def search_one_word(self, input):
        print(input)
        sorted_set_id = self.get_set_id(input)
        print(sorted_set_id)
        for id in self.r.zrevrange(sorted_set_id, 0, 5):
            yield self.r.hget(id, 'title')

    def remove_prefix(self, set_id, hash_id, ):
        last_ele, score = self.r.zrange(set_id, -1, -1, withscores=True)[0]
        self.r.zrem(set_id, last_ele)
        self.r.zadd(set_id, {hash_id: score + 1})

    def check_set_size(self, set_id):
        curr_set_size = self.r.zcard(set_id)
        if curr_set_size < self.max_set_size:
            return True, curr_set_size
        return False, None

    def update_score(self, selected_word, prefix):
        pipe = self.r.pipeline()
        sorted_set_id = self.get_set_id(prefix)
        hash_id = self.get_hash_id(selected_word)
        status, set_size = self.check_set_size(sorted_set_id)
        if not self.check_existence(sorted_set_id):
            if status:
                pipe.zadd(sorted_set_id, {hash_id: 1})
                pipe.hset(hash_id, "title", selected_word)
            else:
                self.remove_prefix(sorted_set_id, hash_id, pipe)
        pipe.zincrby(sorted_set_id, 1, hash_id)
        pipe.execute()

    def get_set_id(self, word):
        return "tmp:" + str(uuid.uuid5(uuid.NAMESPACE_OID, word))

    def get_hash_id(self, word):
        return str(uuid.uuid5(uuid.NAMESPACE_OID, word))

    def search_multiple_word(self, input):
        ''' Does not work as of 04012020'''
        words = input.split(" ")
        if words == []:
            return self.search_one_word("sci")
        if len(words) < 2:
            return self.search_one_word(input)

        sab = self.r.zinterstore(self.get_set_id(input), list(map(self.get_set_id, words)))
        print(sab)
        self.r.expire(self.get_set_id(input), 2700)
        keys = self.r.zrange(self.get_set_id(input), 0, -1)
        result = list()
        for k in keys:
            result.append(self.r.hget(k, 'title').decode("utf-8"))
        return result

    def read_basic_word_file(self, cap=20):
        with open("../deployment/corpus/master.txt", "r") as f:
            for line in f:
                word = line.strip()
                if len(word) > cap or word.isspace():
                    pass
                yield line.strip()

    def create_basic_prefix(self):
        for word in self.read_basic_word_file(20):
            self.add_new_word(word)


if __name__ == "__main__":
    s = SearchCache()
    for s in s.search_multiple_word("appl ap"):
        print(s)
    # s.create_basic_prefix()
# schema a hash entry where its string:"" and id:""
# First create prefixes before launching redis
# Accept some string from the user and create an associated score and the id
# If string is more than one word, split into individual and then take the intersection of
# all the sorted sets.
# Then iterate over the zrange return and hget with the associated key to get the string recomendation
