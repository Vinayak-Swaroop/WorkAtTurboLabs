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
    publisher.publish(channel='URLs',key=Dev.getURL())
    
if __name__==__main__:
    start=time.time()
    HOST=sys.argv[1]
    PORT=sys.argv[2]
    DB=sys.argv[3]
    StoreLocation=sys.argv[4]
    FileLocation=sys.argv[5]
    asyncio.run(schedule())
    end=time.time()
    print(end-start)