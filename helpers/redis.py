import aioredis, pickle
from config import REDIS_URI

redis = aioredis.from_url(REDIS_URI)

def dump(value):
	return pickle.dumps(value)

def load(value):
	return pickle.loads(value) if value else None

class Redis:		
    @classmethod
    async def set(cls,key,value):
        await redis.set(key,dump(value))
    
    @classmethod
    async def get(cls,key):
        value = load(await redis.get(key))    
        return value
    
    @classmethod
    async def setRaw(cls,key,value):
        await redis.set(key,value)
    
    @classmethod
    async def getRaw(cls,key):
        value = await redis.get(key)
        return value.decode('utf-8') if value else None

    @classmethod
    async def clear(cls,key):
        await redis.delete(key)

    @classmethod
    async def clearRedis(cls):
        for key in redis.scan_iter():
            redis.delete(key)

    @classmethod
    async def scheduleClear(cls,key):
        clearList = cls.get('clearList')
        if not clearList: clearList = []
        clearList.append(key)
        cls.save('clearList',clearList)

    @classmethod
    async def clearList(cls):
        clearList = cls.get('clearList')
        if clearList: 
            for key in clearList: cls.clear(key)
            cls.clear('clearList')


