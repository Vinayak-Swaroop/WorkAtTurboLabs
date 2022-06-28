import redis
import asyncio
import ScrapeEngine
import time
import sys
URL='https://dmoz-odp.org/Science/'
HOST='127.0.0.1'
PORT=6379
DB=1
async def main():
    url_list=redis.StrictRedis(host=HOST,port=PORT,db=DB)
    URL_List=['/Science/Reference/']
    # URL_List=['/Science/Agriculture/', '/Science/Anomalies_and_Alternative_Science/', '/Science/Astronomy/', '/Science/Biology/', '/Science/Chemistry/', '/Science/Earth_Sciences/', '/Science/Environment/', '/Science/Math/', '/Science/Physics/', '/Science/Science_in_Society/', '/Science/Social_Sciences/', '/Science/Technology/', '/Science/Academic_Departments/', '/Science/By_Region/', '/Science/Chats_and_Forums/', '/Science/Directories/', '/Science/Educational_Resources/', '/Science/Employment/', '/Science/Events/', '/Science/Instruments_and_Supplies/', '/Science/Methods_and_Techniques/', '/Science/News_and_Media/', '/Science/Organizations/', '/Science/People/', '/Science/Publications/', '/Science/Reference/', '/Science/Research_Groups_and_Centers/', '/Science/Search_Engines/', '/Science/Software/']    
    for i in range(len(URL_List)):
        new_url=URL+URL_List[i].replace(URL.replace('https://dmoz-odp.org',''),'')
        URL_List[i]=new_url
        url_list.set(new_url,'false')
    print(URL_List)
    for key in url_list.keys():
        if key.decode() not in URL_List:
            url_list.delete(key)
        else:
            print(key.decode(),url_list.get(key).decode())

    # print(url_list.get('scrapped'),
    # url_list.get('unscrapped'),
    # url_list.get('inscrap'))

if __name__=='__main__':
    if len(sys.argv)>=2:
        HOST=str(sys.argv[1])
    if len(sys.argv)>=3:
        PORT=int(sys.argv[2])
    if len(sys.argv)>=4:
        DB=int(sys.argv[3])
    print("HOST= {} PORT= {} DB={}".format(HOST,PORT,DB))
    start=time.time()
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    end=time.time()
    print(end-start)