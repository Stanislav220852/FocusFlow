import redis.asyncio as redis
from src.core.config import settings

# Глобальная переменная для клиента
redis_client: redis.Redis | None = None

async def init_redis():
    """Инициализация пула соединений при старте приложения"""
    global redis_client
    redis_client = redis.from_url(
        settings.REDIS_URL, 
        encoding="utf-8", 
        decode_responses=True # Чтобы получать строки, а не байты
    )

async def close_redis():
    """Закрытие соединений"""
    if redis_client:
        await redis_client.close()

# Зависимость для эндпоинтов
async def get_redis() -> redis.Redis:
    if redis_client is None:
        raise ConnectionError("Redis client is not initialized. Check lifespan in main.py")
    return redis_client