import ScrapeEngine
URL='https://dmoz-odp.org/Science/'
ATTRIBUTES={
    'name':'//div[@class="title-and-desc"]/a/div[@class="site-title"]/text()',
    'link':'//div[@class="title-and-desc"]/a/@href',
    'desc':'//div[@class="title-and-desc"]/div[@class="site-descr"]/text()',
}
async def scrapeListingPage(URL,sub_list):
    try:
        listing_parser=await ScrapeEngine.getParser(URL)
        """ Get a page_parser and search for URLs on the page.
            If the page has listings then parse them
            If it leades to further sub-categories, then recursively add those category URLs to be parsed by the same function"""
        print(URL)
        try:
            for text in listing_parser.xpath('//span[@class="header-text"]/text()'):
                if text.lower()=='sites':
                    print('Sub_Called')
                    sub_list.append(await scrapeFinalPage(URL))
        except IndexError:
            return
        except Exception as e:
            print(e)
            return
        for url in listing_parser.xpath('//div[@class="cat-item"]//i[@class="catIcon fa fa-folder-o"]/../../@href'):  #Further sub-category URLs
            await scrapeListingPage(URL+url.replace(URL.replace('https://dmoz-odp.org',''),''),sub_list)
        return sub_list
    except Exception as e:
        print(e)

async def scrapeFinalPage(URL):  
    try:
        global ATTRIBUTES
        page_parser=await ScrapeEngine.getParser(URL)
        product=dict()
        for key in ATTRIBUTES.keys():
            temp=page_parser.xpath(ATTRIBUTES[key])
            sub=[]
            # print(temp)
            for i in temp:
                if i=='\n':
                    continue
                sub.append(i.lstrip('\r\n\t').lstrip().rstrip().rstrip('\r\n\t'))
            product[key]=sub
        sub_list=[]
        for i in range(len(product['name'])):
            prod=dict()
            for key in ATTRIBUTES.keys():
                prod[key]=product[key][i]
            sub_list.append(prod)
        return sub_list
    except Exception as e:
        print(e)