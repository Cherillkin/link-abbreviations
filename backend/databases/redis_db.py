import redis
import json
from typing import Optional, Any, cast
from backend.config.config import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_client = redis.Redis(
    host=cast(str, REDIS_HOST),
    port=cast(int, REDIS_PORT),
    db=cast(int, REDIS_DB),
    decode_responses=True,
)


def save_user_to_redis(user_id: int, user_data: dict) -> None:
    key = f"user:{user_id}"
    redis_client.set(key, json.dumps(user_data))


def get_user_from_redis(user_id: int) -> Optional[Any]:
    key = f"user:{user_id}"
    user_json = redis_client.get(key)
    if user_json:
        return json.loads(user_json)
    return None
