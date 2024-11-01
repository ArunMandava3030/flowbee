# src/queue_manager.py

import redis

class QueueManager:
    def __init__(self, host="localhost", port=6379):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=0)

    def add_profiles(self, profile_urls):
        for url in profile_urls:
            self.redis_client.lpush("profile_queue", url)

    def get_next_profile(self):
        return self.redis_client.rpop("profile_queue").decode("utf-8")
