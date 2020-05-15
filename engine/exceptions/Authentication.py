import os
from datetime import datetime
from flask import jsonify
from pathlib import Path

home = str(Path.home())
path = home + '/csc480/deployment/excep/'


def handle_auth(e):
    write_log(e)
    return jsonify({'error':str(e),'help':"Please Try again with an additional Token."}), 401


def malformed_url_query(e):
    '''Raised when the Redis Cache queries return None.'''
    write_log(e)
    return jsonify(error=str(e)), 501

def write_log(msg):
    curr_date = datetime.today().strftime('%Y-%m-%d-%H-%M %Z')
    with open(path + curr_date + ".excep", "w+") as f:
        f.write(str(msg))
        f.write("\n")

def generic_exception(e):
    '''
    Write the stack trace to file and returns an Internal Server Error 500
    :param e:
    :return:
    '''
    stack_trace = e.orginal_exception
    write_log(stack_trace)
    return jsonify(error=str(e)), 500
