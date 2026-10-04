import json
import logging
import time
from typing import Optional, Dict, Any, List, Tuple
import redis.asyncio as aioredis
from fakeredis import aioredis as fake_aioredis
from app.config import settings

logger = logging.getLogger("ticketlocal.redis")

class RedisManager:
    def __init__(self):
        self._client: Optional[aioredis.Redis] = None
        self._is_fallback: bool = False

    async def get_client(self) -> aioredis.Redis:
        if self._client is None:
            try:
                client = aioredis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True,
                    socket_connect_timeout=0.8,
                )
                await client.ping()
                self._client = client
                self._is_fallback = False
                logger.info(f"Connected to Redis server at {settings.REDIS_URL}")
            except Exception as e:
                logger.info(f"Using in-memory FakeRedis engine: {e}")
                self._client = fake_aioredis.FakeRedis(decode_responses=True)
                self._is_fallback = True
        return self._client

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None

redis_manager = RedisManager()

def make_lock_key(show_id: int, seat_id: int) -> str:
    return f"lock:show_{show_id}:seat_{seat_id}"

async def acquire_atomic_seat_locks(
    show_id: int,
    seat_ids: List[int],
    user_id: str,
    ttl_seconds: int = settings.REDIS_LOCK_TTL_SECONDS,
) -> Tuple[bool, List[int]]:
    """
    Atomically acquires temporary locks for multiple seat IDs for a show.
    Returns (success: bool, conflicting_seat_ids: List[int])
    """
    if not seat_ids:
        return True, []

    client = await redis_manager.get_client()
    keys = [make_lock_key(show_id, sid) for sid in seat_ids]

    pipe = client.pipeline()
    for k in keys:
        pipe.get(k)
    vals = await pipe.execute()

    conflicts = []
    for sid, val in zip(seat_ids, vals):
        if val is not None and str(val) != str(user_id):
            conflicts.append(sid)

    if conflicts:
        return False, conflicts

    # All clear - set holds
    pipe = client.pipeline()
    for k in keys:
        pipe.set(k, str(user_id), ex=ttl_seconds)
    await pipe.execute()
    return True, []

async def release_seat_locks(
    show_id: int,
    seat_ids: Optional[List[int]],
    user_id: str,
) -> int:
    client = await redis_manager.get_client()
    if seat_ids is None:
        pattern = f"lock:show_{show_id}:seat_*"
        keys = await client.keys(pattern)
        if not keys:
            return 0
        pipe = client.pipeline()
        for k in keys:
            pipe.get(k)
        vals = await pipe.execute()
        del_keys = [k for k, val in zip(keys, vals) if str(val) == str(user_id)]
        if del_keys:
            return await client.delete(*del_keys)
        return 0
    else:
        released = 0
        for sid in seat_ids:
            k = make_lock_key(show_id, sid)
            val = await client.get(k)
            if val is not None and str(val) == str(user_id):
                if await client.delete(k):
                    released += 1
        return released

async def check_user_holds(show_id: int, seat_ids: List[int], user_id: str) -> Tuple[bool, Optional[int]]:
    if not seat_ids:
        return False, None

    client = await redis_manager.get_client()
    pipe = client.pipeline()
    for sid in seat_ids:
        k = make_lock_key(show_id, sid)
        pipe.get(k)
        pipe.ttl(k)
    results = await pipe.execute()

    min_ttl = None
    for i in range(0, len(results), 2):
        val = results[i]
        ttl = results[i + 1]
        if val is None or str(val) != str(user_id) or ttl is None or ttl <= 0:
            return False, None
        if min_ttl is None or ttl < min_ttl:
            min_ttl = ttl

    return True, min_ttl

async def get_all_locks_for_show(show_id: int) -> Dict[int, Dict[str, Any]]:
    client = await redis_manager.get_client()
    pattern = f"lock:show_{show_id}:seat_*"
    keys = await client.keys(pattern)
    if not keys:
        return {}

    pipe = client.pipeline()
    for k in keys:
        pipe.get(k)
        pipe.ttl(k)
    results = await pipe.execute()

    locks = {}
    for i, k in enumerate(keys):
        val = results[i * 2]
        ttl = results[i * 2 + 1]
        if val is not None and ttl is not None and ttl > 0:
            try:
                sid = int(k.split(":seat_")[1])
                locks[sid] = {
                    "user_id": str(val),
                    "remaining_ttl_seconds": ttl,
                }
            except Exception:
                pass
    return locks

async def count_active_locks() -> int:
    client = await redis_manager.get_client()
    keys = await client.keys("lock:show_*:seat_*")
    return len(keys)

async def flush_all_seat_locks() -> int:
    client = await redis_manager.get_client()
    keys = await client.keys("lock:show_*:seat_*")
    if not keys:
        return 0
    return await client.delete(*keys)
