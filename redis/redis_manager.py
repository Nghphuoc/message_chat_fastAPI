import aioredis

from model.schema import MessageRequest

REDIS_URL = "redis://localhost:6379"

class RedisPubSub:


    def __init__(self):
        self.redis = None


    async def connect(self):
        self.redis = await aioredis.from_url(REDIS_URL, decode_responses=True)


    async def subscribe(self, channel: str):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        return pubsub


    # use for message service add to database
    async def publish(self, channel: str, message: str):
        await self.redis.publish(channel, message)
