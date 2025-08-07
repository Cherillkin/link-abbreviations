import redis
import json
from backend.config.config import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def save_user_to_redis(user_id: int, user_data: dict):
    key = f"user:{user_id}"
    redis_client.set(key, json.dumps(user_data))

def get_user_from_redis(user_id: int):
    key = f"user:{user_id}"
    user_json = redis_client.get(key)
    if user_json:
        return json.loads(user_json)
    return None