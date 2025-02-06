import scrapy
import csv
import re

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
        model_auta = response.css("div.detail-hero__info__content__section > section > h1::text").get()
        verze_modelu = response.css("div.detail-hero__info__content__section > section > p.text-M::text").get()
        cena = response.css("div.detail-hero__info__content__info > p.text-h1.highlighted::text").get()
        datum_registrace = response.css('div.detail-hero__info__boxes > div.detail-hero__info__box:nth-of-type(1)::text').getall()
        najezd = response.css('div.detail-hero__info__boxes > div.detail-hero__info__box:nth-of-type(2)::text').getall()
        stk = response.xpath("//div[@class='detail-box-M']/div/div[3]/text()").getall()
        stav = response.xpath("//span[@class='detail-info__row__state__text']/text()").get().strip()
        vykon = response.xpath('//div[@class="detail-info__col"][1]/div[2]/div[1]/div[1]/text()').getall()
        objem_motoru = response.xpath('//div[@class="detail-info__col"][1]/div[2]/div[1]/div[2]/text()').getall()
        typ_paliva = response.xpath('//div[@class="detail-info__col"][1]/div[2]/div[1]/div[3]/text()').getall()
        typ_prevodovky = response.xpath('//div[@class="detail-info__col"][1]/div[2]/div[1]/div[4]/text()').getall()
        typ_karoserie = response.xpath('//div[@class="detail-info__col"][2]/div[2]/div[1]/div[1]/text()').getall()
        pocet_dveri = response.xpath('//div[@class="detail-info__col"][2]/div[2]/div[1]/div[2]/text()').getall()
        pocet_mist = response.xpath('//div[@class="detail-info__col"][2]/div[2]/div[1]/div[3]/text()').getall()
        barva_exterieru = response.xpath('//div[@class="detail-info__col"][2]/div[2]/div[1]/div[4]/text()').getall()


        # Čištění získaných řetězců
        model_auta = re.sub(r'\s+', ' ', model_auta).strip()
        verze_modelu = re.sub(r'\s+', ' ', verze_modelu).strip()
        #Cena zůstává beze změny
        datum_registrace = ' '.join(datum_registrace).strip().replace(' ', '')
        najezd = ' '.join(najezd).strip().replace(' ', '')
        stk = re.sub(r"\s+", " ", " ".join(stk).strip())
        #Stav zůstává beze změny
        vykon = re.sub(r"\s+", " ", " ".join(vykon).strip())
        objem_motoru = re.sub(r"\s+", " ", " ".join(objem_motoru).strip())
        typ_paliva = re.sub(r"\s+", " ", " ".join(typ_paliva).strip())
        typ_prevodovky = re.sub(r"\s+", " ", " ".join(typ_prevodovky).strip())
        typ_karoserie = re.sub(r"\s+", " ", " ".join(typ_karoserie).strip())
        pocet_dveri = re.sub(r"\s+", " ", " ".join(pocet_dveri).strip())
        pocet_mist = re.sub(r"\s+", " ", " ".join(pocet_mist).strip())
        barva_exterieru = re.sub(r"\s+", " ", " ".join(barva_exterieru).strip())

        # Uložení dat do csv souboru
        with open("data/cars.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([model_auta, verze_modelu, cena, datum_registrace, najezd, stk, stav, vykon,
                             objem_motoru, typ_paliva, typ_prevodovky, typ_karoserie, pocet_dveri, pocet_mist,
                             barva_exterieru])