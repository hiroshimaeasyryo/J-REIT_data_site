import os
import redis
from rq import Worker, Queue, Connection


listen = ['high', 'default', 'low']
redis_url = os.getenv('REDISTOGO_URL', 'redis://redistogo:621717682c6f059a39f1750f1a52b236@hammerjaw.redistogo.com:11524/')
conn = redis.from_url(redis_url)


if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()