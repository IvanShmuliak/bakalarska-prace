import scrapy
import csv

class TipcarsSpider(scrapy.Spider):
    name = "tipcars_urls"
    start_urls = ["https://www.tipcars.com/bmw?str=1-20/"]

    car_urls = []  # Proměnná na úrovni třídy pro ukládání URL odkazů na inzeraty

    def parse(self, response):
        try:
            car_links = response.css("a[data-offer-listing-id-param]::attr(href)").getall()
            self.car_urls = list({response.urljoin(link) for link in car_links})

        except Exception as e:
            self.logger.error(f"Chyba při získávání odkazů na auta: {e}")
            return  # Ukončení iterace, pokud dojde k chybě

        # Zastaví pokud nová stránka neobsahuje inzeráty
        if car_links:

            # Získání aktuálního čísla stránky
            current_page = int(response.url.split("?str=")[1].split("-")[0])

            # Logování URL po nasbírání ze stránky
            self.logger.info(f"Collected URLs from page: {current_page}")
            for url in self.car_urls:
                self.logger.debug(f"URL: {url}")  # Detailní výpis URL

            # Zápis URL odkazů do csv
            try:
                with open("../data/raw_data/car_urls.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    for url in self.car_urls:
                        writer.writerow([url])
            except Exception as e:
                self.logger.error(f"Chyba při zápisu do CSV souboru: {e}")
                return  # Ukončení, pokud zápis selže

            # Generate the next page URL
            next_page = current_page + 1
            next_page_url = f"https://www.tipcars.com/bmw?str={next_page}-20"
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            self.logger.info("Žádné další odkazy, scraping ukončen.")
