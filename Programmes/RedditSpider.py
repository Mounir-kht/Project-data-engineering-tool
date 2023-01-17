
import scrapy

class RedditSpider(scrapy.Spider):
    name = "Reddit"
    start_urls = ["https://www.reddit.com/r/Trading/?f=flair_name%3A%22Stocks%22",]

    def parse(self, response):
        for cit in response.xpath('//div[@data-testid="post-container"]'):
            text_value = cit.xpath('/html//div').extract_first()
            yield { 'text' : text_value }