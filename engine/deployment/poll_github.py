import subprocess
import time, sched
import os
from datetime import datetime


class UpdateServer():
    '''Due to server permissions,Engine couldn't schedule a cronjob to update the server on a schedule.
    We can use python though to execute commands which is used to execute a simple script.
    '''
    
    def create_log(stderr):
            print("loggy")
            curr_date = datetime.today().strftime('%Y-%m-%d-%H-%M-%S %Z')
            env_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'logs','')
            print(env_path)
            file_name = env_path+str(curr_date) + '.log'
            print(file_name)
            with open(file_name, 'w+') as f:
                f.write(str(stderr))


    def check_github(sc):
        '''
        Runs the script to pull from master and updates server.

        Args:
            sc(sched):Scheduler registers and runs the given function.
        Returns:
            None: Scripts runs until terminated.
        '''
        home=os.getenv('HOME')
        script_loc = '/csc480/deployment/updater.sh'
        path = home +script_loc
        pid= str(os.getpid())
        process = subprocess.Popen([path,pid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = process.communicate(timeout=15)  # believe this is blocking
            UpdateServer.create_log(stderr)
            sc.enter(3600, 60,UpdateServer.check_github,(sc,))
        except subprocess.TimeoutExpired as e:
            process.kill()
            UpdateServer.create_log("timeout")
            sc.enter(3600, 60,UpdateServer.check_github,(sc,))
        
if __name__ == '__main__':
    scheder = sched.scheduler(time.time, time.sleep)
    scheder.enter(5, 60, UpdateServer.check_github, (scheder,))
    scheder.run()
