import requests as rq
from pyquery import PyQuery as pq
homeRes = rq.get('https://www.books.com.tw/web/sys_tdrntb/books/?loc=subject_004') #網址為「博客來中文書排行榜」
homeDoc = pq(homeRes.text)

# 主程式
all_dataset = []
homeDoc.make_links_absolute(base_url=homeRes.url)
n = 1

# 針對每個主類別
for eachMainDoc in homeDoc("body  div.mod.type02_s001.clearfix > ul > li > div > a").items():
    print(str(n)+'.',eachMainDoc.text()) #印出主類別
    
    main_dataset = []
    
    #print(eachMainDoc.attr('href')) #主類別的網址
    
    mainCateDoc = pq(eachMainDoc.attr('href'))
    #print(mainCateDoc('body > div.container_24.main_wrap.clearfix > div > div.mod.type02_s003.clearfix > ul > li.here > ul > li > a').text()) #印出主類別中所有子類別
    mainCateDoc.make_links_absolute(base_url=homeRes.url)
    i=1
    
    # 不是每個主類別都有子類別
    ## (1) 只有「主類別」
    if mainCateDoc('.here > .sub_list > li > a').text() == '':
        for eachMainItemDoc in mainCateDoc(".type02_m035 .clearfix > .item").items():
            price_set = []
            mainItemDict = {}
            mainItemDict['ranking category'] = eachMainDoc.text()
            mainItemDict['TOP'] = eachMainItemDoc("strong.no").text()
            mainItemDict['bookname'] = eachMainItemDoc("h4 a").text()
            mainItemDict['author'] = eachMainItemDoc(".msg a").text()
            
            # 有些書沒有打折，所以區分（「discount」+「price」）與（「price」）的情況
            for each_Price in eachMainItemDoc("li.price_a > strong > b").items():
                price_set.append([each_Price])
            if len(price_set) == 2:
                mainItemDict['discount'] = eachMainItemDoc("li.price_a > strong:nth-child({}) > b".format(1)).text()
                mainItemDict['price'] = eachMainItemDoc("li.price_a > strong:nth-child({}) > b".format(2)).text()
            else:
                mainItemDict['price'] = eachMainItemDoc("li.price_a > strong:nth-child({}) > b".format(1)).text()
            
            # 印出結果
            try:
                print('TOP{} {} {} {}折 {}元'.format(mainItemDict['TOP'],mainItemDict['bookname'],mainItemDict['author'],mainItemDict['discount'],mainItemDict['price']))
            except KeyError:
                print('TOP{} {} {} {}元'.format(mainItemDict['TOP'],mainItemDict['bookname'],mainItemDict['author'],mainItemDict['price']))            
            main_dataset.append(mainItemDict)
            all_dataset.append(mainItemDict)
            
    ## (2) 有「主類別」也有「子類別」
    else:  
        for eachSubDoc in mainCateDoc('.here > .sub_list > li > a').items():
            #print(eachSubDoc.attr('href')) #子類別的網址

            sub_dataset = []

            print('('+str(i)+')',eachSubDoc.text()) #印出子類別 ex: (1) 7日暢銷榜
            i += 1
            subCateDoc = pq(eachSubDoc.attr('href'))

            for eachItemDoc in subCateDoc(".type02_m035 .clearfix > .item").items():
                price_set = []
                itemDict = {}
                itemDict['ranking category'] = eachMainDoc.text()
                itemDict['sub_ranking category'] = eachSubDoc.text()
                itemDict['TOP'] = eachItemDoc("strong.no").text()
                itemDict['bookname'] = eachItemDoc("h4 a").text()
                itemDict['author'] = eachItemDoc(".msg a").text()
                
                # 有些書沒有打折，所以區分（「discount」+「price」）與（「price」）的情況
                for each_Price in eachItemDoc("li.price_a > strong > b").items():
                    price_set.append([each_Price])
                if len(price_set) == 2:
                    itemDict['discount'] = eachItemDoc("li.price_a > strong:nth-child({}) > b".format(1)).text()
                    itemDict['price'] = eachItemDoc("li.price_a > strong:nth-child({}) > b".format(2)).text()
                else:
                    itemDict['price'] = eachItemDoc("li.price_a > strong:nth-child({}) > b".format(1)).text()
                
                #印出結果
                try:
                    print('TOP{} {} {} {}折 {}元'.format(itemDict['TOP'],itemDict['bookname'],itemDict['author'],itemDict['discount'],itemDict['price']))
                except KeyError:
                    print('TOP{} {} {} {}元'.format(itemDict['TOP'],itemDict['bookname'],itemDict['author'],itemDict['price']))    
                sub_dataset.append(itemDict)
                all_dataset.append(itemDict)
    n += 1
