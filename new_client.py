import redis
import time
import Dev
import asyncio
import ScrapeEngine
import traceback
import io
import sys
import pickle

URL=Dev.URL
HOST='127.0.0.1'
PORT=6379
DB=1


class ListEmptyException(Exception):
    def __str__(self):
        return "No URLs found on server...returning"

def writeToFile(File_Name,sub_list):
    ScrapeEngine.openFile(File_Name)
    ScrapeEngine.setFileHeaders(Dev.ATTRIBUTES.keys())
    ScrapeEngine.writeToFile(sub_list)
    ScrapeEngine.closeFile()

async def startClient():
    try:
        url=""
        url_list=redis.StrictRedis(host=HOST,port=PORT,db=DB)
        if not url_list.keys(): #List is empty
                raise ListEmptyException
        for key in url_list.keys():
            if key.decode() =='Final Result':
                continue
            if 'Scrape' in key.decode():
                continue
            if  url_list.get(key).decode()=='false':
                url=key.decode()
                url_list.set(key,'true')
                break
        if url=="":
            print("All scrapped")
            return
        print(url)
        sub_list=[]
        await Dev.scrapeListingPage(url, sub_list)           #!Change this to be more flexible
        url_list.set(('Scrape'+url.replace(URL,'')).replace('/','_'),pickle.dumps(sub_list))
        if url_list.exists('Final List'):
            url_list.set('Final Result',pickle.dumps(pickle.loads(url_list.get('Final Result')).append(sub_list)))
        else:
            url_list.set('Final Result',pickle.dumps(sub_list))

        await ScrapeEngine.closeSession()
        return sub_list
    except ListEmptyException as e:
        print(e)
        return
    except Exception as e:
        errors = io.StringIO()
        traceback.print_exc(file=errors)
        contents = str(errors.getvalue())
        print(contents)
        errors.close()
        print(e)
        input()

if __name__=='__main__':
    try:
        if len(sys.argv)>=2:
            HOST=str(sys.argv[1])
        if len(sys.argv)>=3:
            PORT=int(sys.argv[2])
        if len(sys.argv)>=4:
            DB=int(sys.argv[3])
        print("HOST= {} PORT= {} DB={}".format(HOST,PORT,DB))
        print('Started Client')
        start=time.time()
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(startClient())
        end=time.time()
        print(end-start)
    except Exception as e:
        print(e)
