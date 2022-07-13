import redis
import asyncio
obj=redis.StrictRedis(host="10.0.0.168",port=6379,db=2)
async def main():
    for key in obj.keys():
        print(key.decode())
        obj.delete(key.decode())
    print("done")

if __name__=="__main__":
    asyncio.run(main())