import redis
import time
import Dev
import asyncio
import ScrapeEngine
import traceback
import io
import sys
import pickle

URL=Dev.getURL()
HOST=None
PORT=None
StoreLocation=None
FileLocation=None

def schedule():
    publisher=redis.StrictRedis(host=HOST,port=PORT,db=0)
    
if __name__==__main__:
    start=time.time()
    HOST=sys.argv[1]
    PORT=sys.argv[2]
    StoreLocation=sys.argv[3]
    FileLocation=sys.argv[4]
    asyncio.run(schedule())
    end=time.time()
    print(end-start)