from endpoints import Auxiliary
from suggestions.prefix_cache import SearchCache
from suggestions.task_queue import TaskQueue
from flask import jsonify, abort
from flask_restful import Resource, reqparse


class TextSuggestion(Resource):
    def __init__(self):
        self.s = SearchCache()
        self.tq = TaskQueue()
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        parser = self.create_parser()
        ret = parser.parse_args()
        user_entry = ret.get("query", "med")
        result = list()
        #self.tq.add_function(self.s.add_new_word,user_entry)
        for suggest in self.s.search_multiple_word(user_entry):
            result.append(str(suggest))
        return jsonify({"suggestions": result})

    @Auxiliary.auth_dec
    def post(self,**kwargs):
        parser = self.create_parser()

        ret = parser.parse_args()
        user_entry = ret.get("query", None)
        prefix = ret.get("prefix", None)
        if user_entry is None or prefix is None:
            abort(501, description="The Variables were malformed.Please try again.")
        self.s.update_score()

    def create_parser(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("query", type=str, default=True)
        parser.add_argument("prefix", type=str)
        return parser
