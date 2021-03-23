import os
import redis
from rq import Worker, Queue, Connection


listen = ['high', 'default', 'low']
redis_url = os.getenv('redis://redistogo:621717682c6f059a39f1750f1a52b23', 'redis://localhost:6379')
conn = redis.from_url(redis_url)


if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()