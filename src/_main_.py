from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from src.spiders.tipcar_urls import TipcarsSpider
from src.spiders.car_details import CarDetailsSpider

# Nastavení logování
configure_logging()
runner = CrawlerRunner(settings={
        "ROBOTSTXT_OBEY": True,  # Respektování souboru robots.txt
        "DOWNLOAD_DELAY": 1,     # Prodleva mezi požadavky
        "CONCURRENT_REQUESTS": 2,  # Omezení paralelních požadavků
        "DEFAULT_REQUEST_HEADERS": {  # Nastavení HTTP hlaviček
            'User-Agent': 'MyAcademicScraper'}
    })

@defer.inlineCallbacks
def run_spiders():
    # Spuštění prvního spidera
    yield runner.crawl(TipcarsSpider)
    # Spuštění druhého spidera jen po dokončení prvního
    yield runner.crawl(CarDetailsSpider)
    # Ukončí reactor po dokončení druhého spidera
    reactor.stop()

if __name__ == "__main__":
    # Spuštění sekvenčního běhu spiderů
    run_spiders()
    reactor.run()
