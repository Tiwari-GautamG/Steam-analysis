import scrapy
from ssteam.ssteam.items import SteamGeneral

class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    allowed_domains = ["store.steampowered.com"]

    def __init__(self, start=0, end=15000, *args, **kwargs):
        super(CrawlerSpider, self).__init__(*args, **kwargs)
        self.start = int(start)
        self.end = int(end)

    def start_requests(self):
        try:
            for i in range(self.start, self.end, 100):
                urls = f'https://store.steampowered.com/search/results/?query&start={i}&count=100&dynamic_data=&force_infinite=1&maxprice=5000&tags=4182&category1=998&supportedlang=english&ndl=1&snr=1_7_7_240_7&infinite=1'
                yield scrapy.Request(url=urls, callback=self.parse_urls)

        except Exception as e:
            self.logger.error(f"Failed to read file: {e}")

    def parse_urls(self, response):
        data = dict(response.json())
        results = data['results_html']
        selector = scrapy.Selector(text=results)
        urls = selector.css('a::attr(href)').getall()
        self.logger.info(f"Extracted {len(urls)} URLs from the page.")
        for i in urls:
            yield scrapy.Request(url=i, callback=self.parse)

    def parse(self, response):
        name = response.css('#appHubAppName::text').get()

        try:
            pstorage = response.xpath("//*[text()= 'Storage:']")[0]
            ppstorage = pstorage.xpath('..')
            storage = ppstorage.xpath('string()').get()
        except IndexError as ie:
            storage = None

        try:
            pmemory = response.xpath("//*[text()= 'Memory:']")[0]
            ppmemory = pmemory.xpath('..')
            memory = ppmemory.xpath('string()').get()
        except IndexError as ie:
            memory = None

        prc_blk = response.css('.game_area_purchase_game')
        try:
            disc_pct = prc_blk.css('.discount_pct::text').get()
            disc_amt = prc_blk.css('.discount_final_price::text').get()
            if disc_pct is None or disc_amt is None:
                raise ValueError("Missing discount information")
        except Exception as e:
            disc_pct = None
            disc_amt = response.xpath('//div[@class="game_purchase_price price"] /text()').get()

        rev = response.xpath("//div[@class='user_reviews_summary_bar'] //span/@data-tooltip-html").get()
        dlcyn = response.xpath("//div[@class='game_area_purchase']/div").getall()

        steam = SteamGeneral()
        if len(dlcyn) > 1:
            steam['DLC'] = 'Yes'
        else:
            steam['DLC'] = 'No'

        yr = response.xpath("//div[@class='date'] /text()").get()

        try:
            tgs = response.xpath("//div[@class='glance_tags popular_tags']//a/text()").getall()[:2]
            if len(tgs) < 2:
                raise Exception('Inadequate tags')
        except Exception:
            tgs = [None, None]

        img = response.xpath("//img[@class='game_header_image_full']/@src").get()

        steam['Title'] = name
        steam['RAM'] = memory
        steam['Size'] = storage
        steam['Discount'] = disc_pct
        steam['Price'] = disc_amt
        steam['ReviewsNum'] = rev
        steam['Year'] = yr
        steam['Tag_1'] = tgs[0]
        steam['Tag_2'] = tgs[1]
        steam['Image'] = img
        yield steam



