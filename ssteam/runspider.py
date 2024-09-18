from spiders.crawler import CrawlerSpider
from scrapy.crawler import CrawlerProcess
import multiprocessing


def run_spider(start, end):
    settings = {
        'ITEM_PIPELINES': {
            'ssteam.ssteam.pipelines.SqlStorage': 1,
        },
        'LOG_LEVEL': 'INFO',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'CONCURRENT_REQUESTS': 45,
        'DOWNLOAD_DELAY': 0.08,
    }

    process = CrawlerProcess(settings=settings)
    process.crawl(CrawlerSpider, start=start, end=end)
    process.start()


def main(end, rate):
    job = []
    for i in range(0, end, rate):
        p = multiprocessing.Process(target=run_spider, args=(i, i+rate))
        job.append(p)
        p.start()

    for k in job:
        k.join()


if __name__ == '__main__':
    main(40000, 8000)

