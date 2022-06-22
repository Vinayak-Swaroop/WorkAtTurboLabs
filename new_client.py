import redis
import time
import Dev
import asyncio
import ScrapeEngine
import traceback
import io
import pickle
URL=Dev.URL

def writeToFile(File_Name,sub_list):
    ScrapeEngine.openFile(File_Name)
    ScrapeEngine.setFileHeaders(Dev.ATTRIBUTES.keys())
    ScrapeEngine.writeToFile(sub_list)
    ScrapeEngine.closeFile()

async def startClient():
    try:
        url=""
        url_list=redis.StrictRedis(host='10.0.0.168',port=6379,db=1)
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
        print('Started Client')
        start=time.time()
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(startClient())
        end=time.time()
        print(end-start)
    except Exception as e:
        print(e)
