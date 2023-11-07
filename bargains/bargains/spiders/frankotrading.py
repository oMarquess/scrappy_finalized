'''
The 'frankotradingSpider is designed to extract product data from the Franko Trading website.
It will scrape products by navigating through the categories in the following sequence:
1. Mobile Phones - to collect information on all mobile phone products.
2. Computers - to scrape details related to desktops, laptops, and related computing devices.
3. Accessories - to gather data on product accessories such as cases, chargers, and other peripherals.
4. Appliances - to extract information on home and kitchen appliances.
5. Printers - to collect details on various types of printers available.
Additionally, the scraper will also retrieve promotional banners displayed across these categories.

To scrap from a category, kindly comment out the rest of the code except the preferred category. Then, run scrapy crawl frankotrading -o <frankotrading_data/filename.json>

'''

import scrapy


class FrankotradingSpider(scrapy.Spider):
    name = "frankotrading"
    allowed_domains = ["frankotrading.com"]
    start_urls = ["https://frankotrading.com"]

    def parse(self, response):
        pass
