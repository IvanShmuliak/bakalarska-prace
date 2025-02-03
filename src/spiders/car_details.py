import scrapy
import csv
import re

class CarDetailsSpider(scrapy.Spider):
    name = "car_details"

    def start_requests(self):
        # Načtení URL odkazů z csv souboru
        with open("car_urls.csv", "r") as f:
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
        #fuel_type = response.css("div.fuel::text").get()
        #mileage = response.css("div.mileage::text").get()
        #location = response.css("div.location::text").get()

        # Čištění získaných řetězců


        # Uložení dat do csv souboru
        with open("data/cars.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([car_model, model_version, price, registration_date, mileage])
            #writer.writerow([car_model, model_version, price, fuel_type, mileage, location, response.url])