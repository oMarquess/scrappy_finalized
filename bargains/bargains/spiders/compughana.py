'''
The CompughanaSpider is designed to extract product data from the Franko Trading website.
It will scrape products by navigating through the categories in the following sequence:

   ### MOBILE_PHONES ####
#     #base_url = "https://compughana.com/phones-tablets.html"
#     ### IT NETWORKING ####
#     #base_url = "https://compughana.com/it-networking.html"
#     # ### HB_NETWORKING ####
#     base_url = "https://compughana.com/hp-products.html"
#     # ### LG_NETWORKING ####
#     # base_url = "https://compughana.com/lg-products.html"
#     # ### HOME_APPLIANCES ####
#     # base_url = "https://compughana.com/home-appliance.html"
#     # ### SMALL_APPLIANCES ####
#     # base_url = "https://compughana.com/small-appliances.html"
#     # ### OTHER_APPLIANCES ####
#     # base_url = "https://compughana.com/others.html"

To scrap from a category, kindly comment out the rest of the code except the preferred category. Then, run scrapy crawl frankotrading -o <frankotrading_data/filename.json>

'''





import scrapy
import re

class CompughanaSpider(scrapy.Spider):
    name = "compughana"
    allowed_domains = ["compughana.com"]
    
    #Fix the base_url for the category here
    base_url = "https://compughana.com/others.html"
    start_urls = [base_url]

    def __init__(self, *args, **kwargs):
        super(CompughanaSpider, self).__init__(*args, **kwargs)
        # Initialize an empty set to keep track of seen product titles
        self.seen_titles = set()

        # cookies and headers 

        self.cookies = {
            "PHPSESSID" : "pb7nuh2m766qn77s5n3c386qsl",
            "_gcl_au" : "1.1.168168202.1698929280", 
            "_fbp" : "fb.1.1698929280611.2069841994",
            "_gid" : "GA1.2.1342357255.1698929281",
            "form_key" : "aTlBHTfu9Mb9tuxB",
            "mage-translation-storage" : "%7B%7D",
            "mage-translation-file-version" : "%7B%7D",
            "mage-cache-storage" : "%7B%7D",
            "mage-cache-storage-section-invalidation" : "%7B%7D",
            "mage-cache-sessid" : "true",
            "mage-messages" : "",
            "recently_viewed_product" : "%7B%7D",
            "recently_viewed_product_previous" : "%7B%7D",
            "recently_compared_product" : "%7B%7D",
            "recently_compared_product_previous" : "%7B%7D",
            "product_data_storage" : "%7B%7D",
            "form_key" : "aTlBHTfu9Mb9tuxB",
            "section_data_ids" : "%7B%22cart%22%3A1698929283%7D",
            "_ga" : "GA1.2.759686825.1698929280",
            "_ga_P01SBF5218" : "GS1.1.1698929279.1.1.1698930216.60.0.0"
        }
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            #"referrer": "https://compughana.com/phones-tablets.html?",
            "referrer": "https://compughana.com/hp-products.html"
        }

    def parse(self, response):
        # Extract products
        products = response.css('li.item.product')
        for product in products:
            product_title = product.css('strong.product-item-name a::text').get()
            # Check if this title has already been scraped
            if product_title in self.seen_titles:
                self.logger.info('Duplicate item found: %s', product_title)
                return  # Stop the spider if a duplicate is found
            
            # Add the title to the set of seen titles
            self.seen_titles.add(product_title)
            
            product_data = {
                'title': product_title,
                'price': product.css('span.price::text').get(),
                'url': product.css('div.product.photo a::attr("href")').get(),
                'photo': product.css('img.product-image-photo::attr(src), img.product-image-photo::attr(data-src)').get()
            }

            yield scrapy.Request(
                url=product_data['url'],
                callback=self.parse_product_details,
                meta={'product_data': product_data},
                headers=self.headers,
                cookies=self.cookies
            )

        # Pagination logic
        load_more = response.css('a.btn-load-more').get()
        if load_more:
            current_page_number = response.meta.get('page', 1)
            next_page_number = current_page_number + 1
            next_page_url = f"{self.base_url}?p={next_page_number}"

            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse,
                headers=self.headers,
                cookies=self.cookies,
                meta={'page': next_page_number}
            )
        else:
            self.logger.info('No more pages to load.')

    def parse_product_details(self, response):
        # Retrieve product data passed from the list page
        product_data = response.meta['product_data']

        # Extract product details
        description_html = response.css('div[itemprop="description"]').get()
        if description_html:
            description_text = re.sub('<[^<]+?>', ' ', description_html)
            description_text = re.sub('\s+', ' ', description_text).strip()
            product_data['description'] = description_text
        else:
            product_data['description'] = None

        # Extract availability
        availability = response.css('.product-info-stock-sku .stock.available span::text').getall()
        product_data['availability'] = availability[-1].strip() if availability else 'No information'

        # Extract additional images - Just too much is astake here, Ignore
        # image_urls = response.css('.fotorama__stage__frame > img::attr(src)').getall()
        # product_data['additional_images'] = [response.urljoin(url) for url in image_urls]

        yield product_data


###### TO RUN ANY CRAWL #######
# scrapy crawl {spidername} -o ../data/{spidername}/{category}.json
# Eg: scrapy crawl compughana -o ../data/compughana/appliances.json