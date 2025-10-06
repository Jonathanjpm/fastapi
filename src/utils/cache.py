import redis, json
from datetime import timedelta
from typing import Optional, Any
from core.config import host_redis, port_redis, db_redis, ttl_redis

class CacheManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=host_redis,
            port=port_redis,
            db=db_redis,
            decode_responses=True
        )
        self.default_ttl = int(ttl_redis)
    
    def get(self, key: str) -> Optional[Any]:
        cache_key = key
        try:
            cached_data = self.redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
            return None
        except Exception:
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        cache_key = key
        try:
            if ttl is None:
                ttl = self.default_ttl
            
            serialized_value = json.dumps(value, default=str)
            return self.redis_client.setex(
                cache_key, 
                timedelta(seconds=ttl), 
                serialized_value
            )
        except Exception:
            return False
    
    def invalidate(self, key: str) -> bool:
        cache_key = key
        try:
            return bool(self.redis_client.delete(cache_key))
        except Exception:
            return False

cache = CacheManager()