import subprocess,os
from flask_restful import Resource
from flask import jsonify
from endpoints import Auxiliary

class Status(Resource):
    def __init__(self):
        self.path= os.getenv('HOME')+'/csc480/deployment/excep'
    @Auxiliary.auth_dec
    def get(self,**kwargs):
        process = subprocess.Popen(['git', 'log' ,'-1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = process.communicate(timeout=20)  # believe this is blocking
            return jsonify({"version":stdout.decode('UTF-8'),"recent":str(self.read_most_recent())}

                           )
        except subprocess.TimeoutExpired as e:
            process.kill()
            return jsonify({"msg":str(e)})

    def get_most_recent_log(self):
        files=os.listdir(self.path)
        full_paths=[os.path.join(self.path,file) for file in files]
        return max(full_paths,key=os.path.getctime)

    def read_most_recent(self):
        file_path=self.get_most_recent_log()
        with open(file_path,'r') as f:
            return str(f.readlines())
