import redis
import pickle
import ScrapeEngine
import Dev
import time
import sys

def getResult(redis_object):
    final_list=pickle.loads(redis_object.get(Dev.getFileName()))
    # print(final_list)
    return final_list

def Write(File_Name,headers,data):
    try:
        ScrapeEngine.openFile(File_Name)
        ScrapeEngine.setFileHeaders(headers)
        ScrapeEngine.writeToFile(data)
        print("Written")
    except Exception as e:
        print(e)
        raise
if __name__ == "__main__":
    try:
        HOST=None
        PORT=None
        DB=None
        start = time.time()
        if len(sys.argv) >= 2:
            HOST = str(sys.argv[1])
        if len(sys.argv) >= 3:
            PORT = int(sys.argv[2])
        if len(sys.argv) >= 4:
            DB = int(sys.argv[3])
        print("HOST= {} PORT= {} DB={}".format(HOST, PORT, DB))
        Write(File_Name=Dev.getFileName(),headers=Dev.getHeaders(),data=(getResult(redis.StrictRedis(host=HOST,port=PORT,db=DB))))
        end = time.time()
        print(end - start)
    except Exception as e:
        print(e)