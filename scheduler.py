import threading
import subprocess
import asyncio
import redis
import time
import ScrapeEngine
import new_client
def spawnClient():   #Creates a subprocess running ScrapClient.py in a new terminal
    subprocess.call('start /wait python new_client.py', shell=True)

async def startServer():  #Creates the socket object and gets a list of URLS to be parsed
    i=0
    url_list=redis.StrictRedis(db=2)
    for url in url_list.keys():
        url_list.set(url,'false')
    tasks=[]
    final_list=[]
    for url in url_list.keys():
        thread=threading.Thread(target=spawnClient)
        thread.start()
        tasks.append(thread)
    for task in tasks:
        task.join()


if __name__=='__main__':
    start=time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(startServer())
    end=time.time()
    print(end-start)
