import scrapy
import csv
import re
from scrapy import Selector

class CarDetailsSpider(scrapy.Spider):
    name = "car_details"

    def start_requests(self):
        # Načtení URL odkazů z csv souboru
        with open("data/car_urls.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                url = row[0]  # Extract the URL from the first column
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Extrakce dat
        car_model = re.sub(r'\s+', ' ', response.css("div.detail-hero__info__content__section > section > h1::text").get()).strip()
        model_version = re.sub(r'\s+', ' ', response.css("div.detail-hero__info__content__section > section > p.text-M::text").get()).strip()
        price = response.css("div.detail-hero__info__content__info > p.text-h1.highlighted::text").get()
        registration_date = ' '.join(response.css('div.detail-hero__info__boxes > div.detail-hero__info__box:nth-of-type(1)::text').getall()).strip().replace(' ', '')
        mileage = ' '.join(response.css('div.detail-hero__info__boxes > div.detail-hero__info__box:nth-of-type(2)::text').getall()).strip().replace(' ', '')
        stk = re.sub(r"\s+", " ", " ".join(response.xpath("//div[@class='detail-box-M']/div/div[3]/text()").getall()).strip())
        #stav
        vykon = re.sub(r"\s+", " ", " ".join(response.xpath('//div[@class="detail-info__col"][1]/div[2]/div[1]/div[1]/text()').getall()).strip())
        objem_motoru = re.sub(r"\s+", " ", " ".join(response.xpath('//div[@class="detail-info__col"][1]/div[2]/div[1]/div[2]/text()').getall()).strip())
        typ_paliva = re.sub(r"\s+", " ", " ".join(response.xpath('//div[@class="detail-info__col"][1]/div[2]/div[1]/div[3]/text()').getall()).strip())
        typ_prevodovky = re.sub(r"\s+", " ", " ".join(response.xpath('//div[@class="detail-info__col"][1]/div[2]/div[1]/div[4]/text()').getall()).strip())
        typ_karoserie = re.sub(r"\s+", " ", " ".join(response.xpath('//div[@class="detail-info__col"][2]/div[2]/div[1]/div[1]/text()').getall()).strip())
        pocet_dveri = re.sub(r"\s+", " ", " ".join(response.xpath('//div[@class="detail-info__col"][2]/div[2]/div[1]/div[2]/text()').getall()).strip())
        pocet_mist = re.sub(r"\s+", " ", " ".join(response.xpath('//div[@class="detail-info__col"][2]/div[2]/div[1]/div[3]/text()').getall()).strip())
        barva_exterieru = re.sub(r"\s+", " ", " ".join(response.xpath('//div[@class="detail-info__col"][2]/div[2]/div[1]/div[4]/text()').getall()).strip())
        #pohon
        #

        # Čištění získaných řetězců


        # Uložení dat do csv souboru
        with open("data/cars.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([car_model, model_version, price, registration_date, mileage, stk, vykon, objem_motoru, typ_paliva, typ_prevodovky, typ_karoserie, pocet_dveri, pocet_mist, barva_exterieru])
            #writer.writerow([car_model, model_version, price, fuel_type, mileage, location, response.url])