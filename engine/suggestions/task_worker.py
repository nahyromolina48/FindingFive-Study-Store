import redis as r
from rq import Worker, Queue, Connection
import sys

listen = ['default']
conn = r.Redis(host='localhost', port=6380, db=0)

if __name__ == "__main__":
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
