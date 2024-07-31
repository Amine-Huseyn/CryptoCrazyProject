import threading
import requests
import time
import asyncio
import aiohttp

def get_data_sync(urls):
    st = time.time()
    json_array = []
    for url in urls:
        json_array.append(requests.get(url).json())
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
    return json_array

class ThreadingDownloader(threading.Thread):
    json_array = []
    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        response = requests.get(self.url)
        self.json_array.append(response.json())
        #print(self.json_array)
        return self.json_array

def getdatathread(urls):
    st = time.time()
    threads = []
    for url in urls:
        t=ThreadingDownloader(url)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


    et = time.time()
    elapsed_time = et - st
    print("Execution time: ", elapsed_time, "seconds")

async def get_data_async_but_as_wrapper(urls):
    st = time.time()
    json_array=[]

    async with aiohttp.ClientSession() as session:
        for url in urls:
            async with session.get(url) as resp:
                json_array.append(await resp.json())
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
    return json_array


async def getdata(session, url, json_array):
    async with session.get(url) as resp:
        json_array.append(await resp.json())


async def get_data_async_concurrently(urls):
    st =time.time()
    json_array =[]

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(getdata(session,url,json_array)))
        await asyncio.gather(*tasks)
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
    return json_array



urls=["https://postman-echo.com/delay/3"]*10
#getdatasync(urls)
#getdatathread(urls)
asyncio.run (get_data_async_but_as_wrapper(urls))#32
asyncio.run (get_data_async_concurrently(urls))