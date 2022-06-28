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
DB=None

def getTempName(url):
    return ("Scrape" + url.replace(URL, "")).replace("/", "_")


def writeToFile(File_Name, sub_list):
    ScrapeEngine.openFile(File_Name)
    ScrapeEngine.setFileHeaders(Dev.ATTRIBUTES.keys())
    ScrapeEngine.writeToFile(sub_list)
    ScrapeEngine.closeFile()


class ListEmptyException(Exception):
    def __str__(self):
        return "No URLs found on server...returning"


async def startClient():
    while True:
        try:
            File_Name = Dev.getFileName()
            url = ""
            url_list = redis.StrictRedis(host=HOST, port=PORT, db=DB)
            store = redis.StrictRedis(host=HOST, port=PORT, db=Dev.getStoreDB())
            if not url_list.keys():  # List is empty
                raise ListEmptyException
            for key in url_list.keys():
                if key.decode() == Dev:
                    continue
                if "Scrape" in key.decode():
                    continue
                if url_list.get(key).decode() == "false":
                    url = key.decode()
                    url_list.set(key, "true")
                    break
            if url == "":
                print("All scrapped")
                await ScrapeEngine.closeSession()
                return
            print("In client: " + url)
            temp_name = getTempName(url)
            sub_list = []

            FuncDic = await Dev.main(url)

            for key in FuncDic.keys():
                if key.lower() == "data":
                    if not FuncDic[key]:
                        continue
                    sub_list.append(FuncDic[key])
                    if store.exists(File_Name):
                        temp = pickle.loads(store.get(File_Name))
                        temp.append(FuncDic[key])
                        store.set(File_Name, pickle.dumps(temp))
                    else:
                        # print(FuncDic)
                        if type(pickle.dumps(FuncDic[key])) == type(None):
                            # print(FuncDic[key])
                            continue
                        store.set(File_Name, pickle.dumps(FuncDic[key]))
                else:
                    for url in FuncDic[key]:
                        url_list.set(url, "false")

            store.set(getTempName(url).replace("/", "_"), pickle.dumps(sub_list))
        except ListEmptyException as e:
            print(e)
            return
        except Exception as e:
            url_list.set(url, "false")
            errors = io.StringIO()
            traceback.print_exc(file=errors)
            contents = str(errors.getvalue())
            print(contents)
            errors.close()
            print(e)
            input()
            return ()
    await ScrapeEngine.closeSession()


if __name__ == "__main__":
    try:
        start = time.time()
        if len(sys.argv) >= 2:
            HOST = str(sys.argv[1])
        if len(sys.argv) >= 3:
            PORT = int(sys.argv[2])
        if len(sys.argv) >= 4:
            DB = int(sys.argv[3])
        print("HOST= {} PORT= {} DB={}".format(HOST, PORT, DB))
        print("Started Client")
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(startClient())
        end = time.time()
        print(end - start)
    except Exception as e:
        print(e)
