import scrapy

class ChurchillQuotesSpider(scrapy.Spider):
    name = "citations de Churchill"
    start_urls = ['https://www.reddit.com/r/Trading/top/?f=flair_name%3A"Stocks"',]

    def parse(self, response):
        for cit in response.xpath('//h3'):
            # text_value = cit.xpath('a/text()').extract_first()
            text_value = cit.xpath("//h3").extract_first()
            yield { 'text' : cit.extract() }


#comment simuler le scroll avec scrapy pour charger plus de posts