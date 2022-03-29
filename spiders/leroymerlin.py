import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://kaliningrad.leroymerlin.ru/search/?q={kwargs.get('search')}/"]

    def parse(self, response: HtmlResponse):
        next = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next:
            yield response.follow(next, callback=self.parse, meta={"handle_httpstatus_all": True})

        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.parse_ads, meta={"handle_httpstatus_all": True})

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('name', '//h1[@itemprop="name"]/span/text()')
        loader.add_xpath('price', '//div[@data-testid="prices_mf-pdp"]//span/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('photos', '//picture[@slot="pictures"]/source[@media="only screen and (min-width: 1024px)"]/@srcset')
        yield loader.load_item()
