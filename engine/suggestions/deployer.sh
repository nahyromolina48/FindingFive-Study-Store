#!/bin/bash
cd ~/redis/redis/
./redis-server  ~/csc480/suggestions/redis.conf & #study lru cache
./redis-server --port 6379 & #prefix cache
./redis-server --port 6380 & #worker and task queue
cd ~/csc480/suggestions/ && python3 task_worker.py &
