# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 12:08:55 2022

@author: Khalnayak
"""

Documentation for the ScrapeEngine
ScrapeEngine is a powerful scraping library. It provides the developer with the following functions:

1.createSession():
    to be used with the keyword 'await'
    used to create a session object which will handle all the requests between the client and the server

2.getParser(URL):
    to be used with the keyword 'await'
    returns an etree.HTML object which can be used to parse the given URL using xpaths and other etree attributes

3.scrapePages(page_list,scrapeFunc):
    to be used with the keywod 'await'
    accepts a list of urls and a the address of scraping function as arguments
    used to quickly parse pages which are to be parsed using the same function and the same arguments
    returns a list of objects returned by the 'scrapeFunc' for each page in page_list

4.openFile(File_Name):
    used to open/create a csv file with name=File_Name passed by the user
    opens the file in append mode

5.setFileHeaders(headers):
    accepts a list of headers
    sets the them as header for the file created using openFile(File_Name,**headers)

6.writeToFile(data):
    can be used to write a single row or multiple rows of data to the csv file
    if 'data' is of type dictionary, then single row is written
    if 'data' is a list of dictionaries, then multiple rows are written

7.closeFile():
    closes the File object opened with openFile(File_Name,**headers)

8.closeSession():
    to be used with the keyword 'await'
    closes the session object opened with createSession()