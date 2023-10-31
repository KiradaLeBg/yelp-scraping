import scrapy


class YelpSpider(scrapy.Spider):
    name = "Yelp"
    allowed_domain = ['www.yelp.com']
    url = 'https://www.yelp.com/search?find_desc=Contractors&find_loc=San%20Francisco%2C%20CA'
    page = 0
    start_urls = ['https://www.yelp.com/search?find_desc=Contractors&find_loc=San%20Francisco%2C%20CA']
    headers = {
    "authority": "yelp.com",
    "method": "GET",
    "path": "/search?find_desc=&find_loc=New+York%2C+NY%2C+%C3%89tats-Unis",
    "scheme": "https",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "Cookie": ""
}

   
    def start_requests(self):
        for url in self.start_urls:
            self.page += 10
            yield scrapy.Request(url,headers=self.headers, callback=self.parse)


    def parse(self, response, **kwargs):
        links = response.css('a.css-19v1rkv::attr(href)').getall()
        print(links)
        trigger = response.xpath("/html/body/yelp-react-root/div/div[4]/div/div/div/div[2]/div/div/p/a").get()
        for link in links:
            if '/biz/' not in link:
                pass
            else:
                self.headers['path'] = link
                if 'https://' in link:
                    yield scrapy.Request(url=link, headers=self.headers, callback=self.get_info)
                else:
                    yield scrapy.Request(url=f'https://yelp.com{link}', headers=self.headers, callback=self.get_info)
        
        
        if not trigger:
            next_page = f'{self.url}&start={self.page}'
            yield scrapy.Request(next_page, headers=self.headers, callback=self.parse)
            self.page += 10
   
    def get_info(self, response):
        website = response.xpath("//p[@class=' css-1p9ibgf']/a[@class='css-1idmmu3']/text()").get()
        yield {"url": website}
