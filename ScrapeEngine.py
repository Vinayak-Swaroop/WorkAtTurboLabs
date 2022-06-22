# -*- coding: utf-8 -*-
"""
Created on 07/06/22

@author: Khalnayak
"""

import asyncio
import aiohttp
import time
import csv
from bs4 import BeautifulSoup as BS
from lxml import etree
session=None
#creating single session for all requests
HEADERS = ({'User-Agent':
			'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
			(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
			'Accept-Language': 'en-US, en;q=0.5'})

File=None #Single file object for all operations
keys=None #List of headers to be written to csv
class FileNotOpenException(Exception):
    def __str__():
        return 'File is not open. Use openFile() to open a new file'

class SessionNotCreatedException:
    def __str__(Exception):
        return 'Session has not been created'

async def createSession():
    global session
    session=aiohttp.ClientSession(headers=HEADERS)

async def getParser(URL): #returns a an etree.HTML object(html parser) for the page 'URL'
    global session
    while True:
        try:
            if type(session)==type(None):
                await createSession()
            async with session.get(URL) as resp:
                page=await resp.text()
                page_parser=etree.HTML(str(BS(page,'html.parser')))
                return page_parser
        except aiohttp.client_exceptions.ClientOSError as e: #If session object is diconnected or timed out
            await session.close()
            await asyncio.sleep(3) #Back off for 3 seconds to prevent another time-out
            session=aiohttp.ClientSession(headers=HEADERS)
        except aiohttp.client_exceptions.ServerDisconnectedError:
            await session.close()
            await asyncio.sleep(3) #Back off for 3 seconds to prevent another time-out
            session=aiohttp.ClientSession(headers=HEADERS)
        except aiohttp.client_exceptions.InvalidURL:
            print("Invalid URL "+URL)
            break
        

async def scrapePages(page_list,scrapeFunc):   
    #product_list=List of urls to be scrapped
    #scrapeFunc=Scraping function to be used to scrape the urls in the product_list
    #use for quickly scrapping multiple urls with the same scrapping function
    tasks=[]
    for page_link in page_list:
        tasks.append(asyncio.ensure_future(scrapeFunc(page_link)))
    sub_list=await asyncio.gather(*tasks)
    return sub_list

def openFile(File_Name):
    global File
    File=open(File_Name+".csv",'w',newline='',encoding='utf-8')

def setFileHeaders(file_headers): #Set headers for the csv file using a list 'file_headers' passed as an argument
    global keys
    while(True):  #Proceed only after the file has been created
        try:
            if File==None:
                raise FileNotOpenException
            keys=file_headers
            dict_writer=csv.DictWriter(File,file_headers)
            dict_writer.writeheader()
            break
        except FileNotOpenException as e:
            print(e)
            print("Do you want to open a file now?")
            ch=input()
            if ch.lower()=='yes' or ch.lower()=='y':
                print("Enter File Name: ")
                File_Name=input()
                openFile(File_Name)

def writeToFile(data): 
    #can write both single or multiple rows to the csv file
    #if data is a dictionary, single row will be written
    #if data is a lsit of dictionaries multiple rows will be written
    global keys
    global File
    while(True):
        try:
            if File==None:
                raise FileNotOpenException
            dict_writer = csv.DictWriter(File, keys)
            if type(data)==type(list()):
                for flist in data:
                    writeToFile(flist)
            elif type(data)==type(dict()):
                dict_writer.writerow(data)
            break
        except FileNotOpenException as e:
            print(e)
            print("Do you want to open a file now?")
            ch=input()
            if ch.lower()=='yes' or ch.lower()=='y':
                print("Enter File Name: ")
                File_Name=input()
                openFile(File_Name)

def closeFile():
    global File
    File.close()

async def closeSession():
    global session
    await session.close()
