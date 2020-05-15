from rq import Queue
import redis as r
from test_server.TestServer import test_queue

class TaskQueue():
    def __init__(self):
        self.que = Queue(connection=r.Redis(host='localhost', port=6380, db=0))

    def add_function(self, func_name, **kwargs):
        job = self.que.enqueue(func_name,result_ttl=3000, **kwargs)
        return job

    def fetch_job(self, job_id):
        cur_job=self.que.fetch_job(job_id)
        return cur_job

if __name__ == "__main__":
    tq = TaskQueue()
    for i in range(10):
        res = tq.add_function(test_queue)
        tq.fetch_job(res.id)

