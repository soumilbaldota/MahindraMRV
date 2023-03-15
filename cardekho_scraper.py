import scrapy
import json
from scrapy.crawler import CrawlerProcess
import os
hello  = [("thar", 14),("scorpio", 47),("xuv700", 16),
("scorpio-classic", 3), ("xuv300", 74), ("bolero",6),
("bolero-neo", 3), ("xuv400-ev", 3),
("kuv-100-nxt", 9), ("alturas-g4",6), ("marazzo",12)]
d = {}
for y in range(len(hello)):
    d[hello[y][0]] = { x:[] for x in range(0,6)}

class MSpider(scrapy.Spider):
    name = 'thar'
    allowed_domains = ['www.carwale.com']
    start_urls = [f'https://www.cardekho.com/mahindra/{y[0]}/user-reviews/{x}'  for  y in hello for x in range(1,y[1])]

    def parse(self, response):
        a = response.xpath('//*[@id="rf01"]/div[1]/div/div[1]/main/div/div[1]/div[2]/section/div/div[2]/ul/li[*]/div/div/div[2]/p/span[1]')
        b = response.xpath('//*[@id="rf01"]/div[1]/div/div[1]/main/div/div[1]/div[2]/section/div/div[2]/ul/li[*]/div/div/div[1]/div/span')
        c = []
        for x in b:
            if(x.get().count("full-fill") == 0):
                c.append(5)
            else:
                c.append(x.get().count("full-fill"))
        b = c
        k = response.url.split('/')[4]
        for x,y in zip(a.getall(),b):
            d[k][y].append(x[6:-7])
        self.updatejson(k)

    def updatejson(self, y):
        if not os.path.isdir(r"./data/cardekho"):
            os.mkdir('data/cardekho')
        with open(f"data/cardekho/{y}.json", "w") as out:
            json.dump(d[y], out)
            out.close()

process = CrawlerProcess (settings={
# "FEEDS": {
#     "emails.json": {"format": "json"} ,
# } ,
'USER_AGENT': 'Mozilla/5.0' ,
})

print ("start Gather_detail")
process.crawl (MSpider)
process.start ()