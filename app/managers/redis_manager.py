import json

from redis.asyncio import Redis

redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)

class RedisCache:
    def __init__(self):
        self.prefix = "dialog_id"

    def _key(self, dialog_id: str):
        return f"{self.prefix}:{dialog_id}"

    async def get_users(self, dialog_id: str):
        user_json = await redis.get(self._key(dialog_id))
        return json.loads(user_json) if user_json else None

    async def cache_users(self, dialog_id: str, user1: str, user2: str, ttl=3600):
        users_json = json.dumps([user1, user2])
        await redis.set(self._key(dialog_id), users_json, ex=ttl)

    async def is_user_allowed(self, dialog_id: str, user_id: str) -> bool:
        users = await self.get_users(dialog_id)
        if users:
            return user_id in users
        return False