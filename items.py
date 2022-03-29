import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose


def fix_price(price_list):
    try:
        result = int(price_list[0].replace(' ', ''))
        return [result, price_list[-1]]
    except:
        return price_list


class LeroyparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    # price = scrapy.Field(input_processor=Compose(fix_price))
    price = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    _id = scrapy.Field()
