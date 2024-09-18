import scrapy


class SteamGeneral(scrapy.Item):
    Title = scrapy.Field()
    RAM = scrapy.Field()
    Size = scrapy.Field()
    Discount = scrapy.Field()
    Price = scrapy.Field()
    ReviewsNum = scrapy.Field()
    DLC = scrapy.Field()
    Year = scrapy.Field()
    Tag_1 = scrapy.Field()
    Tag_2 = scrapy.Field()
    Image = scrapy.Field()
