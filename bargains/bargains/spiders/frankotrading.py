'''
The 'frankotradingSpider is designed to extract product data from the Franko Trading website.
It will scrape products by navigating through the categories in the following sequence:
1. Computers - to scrape details related to desktops, laptops, and related computing devices. 
2. Mobile Phones - to collect information on all mobile phone products.
3. Accessories - to gather data on product accessories such as cases, chargers, and other peripherals.
4. Appliances - to extract information on home and kitchen appliances.
5. Printers - to collect details on various types of printers available.
6 Banners - The advertisements on the homepage


To scrap from a category, kindly comment out the rest of the code except the preferred category. Then, run scrapy crawl frankotrading -o <frankotrading_data/filename.json>

'''

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class FrankoTradingSpider(scrapy.Spider):
    name = 'frankotrading'
    allowed_domains = ['frankotrading.com']

    def start_requests(self):
        # Uncomment the urls for the appropraite product category

                ##### Computers #####
        # url = "https://frankotrading.com/product-category/laptops-desktops/?v=6848ae6f8e78"
                ####  Phones #####
        #url = "https://frankotrading.com/product-category/mobile-phones/?v=6848ae6f8e78"
                #### Accessories #####
        #url = "https://frankotrading.com/product-category/accessories/?v=6848ae6f8e78"
                #### Appliances #####
        #url = "https://frankotrading.com/product-category/appliances/?v=6848ae6f8e78"
                #### Banners ########
        #url = "https://frankotrading.com/product-category/appliances/?v=6848ae6f8e78"
                  ### Printers #######
        #url = "https://frankotrading.com/product-category/printers/?v=6848ae6f8e78"


        self.cookies = {
            "__zlcmid": "1IcmEsVswE4IEC5",
            "sucuri_cloudproxy_uuid_ada8ef2a2": "eb7ce14f2e4fa718f19aa0a774751c7a",
            "PHPSESSID": "9vamo2en014n0uhilfmdcms46k",
            "form_key": "y0uBYKU1VoPlbRab",
            "mage-cache-storage": "%7B%7D",
            "mage-cache-storage-section-invalidation": "%7B%7D",
            "mage-cache-sessid": "true",
            "searchsuiteautocomplete": "%7B%7D",
            "mage-messages": "",
            "recently_viewed_product": "%7B%7D",
            "recently_viewed_product_previous": "%7B%7D",
            "recently_compared_product": "%7B%7D",
            "recently_compared_product_previous": "%7B%7D",
            "product_data_storage": "%7B%7D",
            "section_data_ids": "%7B%22cart%22%3A1698913496%7D",
            "amp_6e403e": "GrbSqKvpyV0ybbzub0DTx-...1he7i4jaf.1he7i5cl2.0.0.0",
        }

        #uncomment the appropraite referer for the set category
        self.headers = {
            "authority": "frankotrading.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            # 'cookie': '__zlcmid=1IcmEsVswE4IEC5; sucuri_cloudproxy_uuid_ada8ef2a2=eb7ce14f2e4fa718f19aa0a774751c7a; PHPSESSID=9vamo2en014n0uhilfmdcms46k; form_key=y0uBYKU1VoPlbRab; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; searchsuiteautocomplete=%7B%7D; mage-messages=; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; section_data_ids=%7B%22cart%22%3A1698913496%7D; amp_6e403e=GrbSqKvpyV0ybbzub0DTx-...1he7i4jaf.1he7i5cl2.0.0.0',
            "dnt": "1",
            "pragma": "no-cache",
            #"referer": "https://frankotrading.com/product-category/laptops-desktops/?v=6848ae6f8e78",
            #"referer": "https://frankotrading.com/product-category/mobile-phones/?v=6848ae6f8e78",
            #"referer": "https://frankotrading.com/product-category/accessories/?v=6848ae6f8e78",
            #"referer": "https://frankotrading.com/product-category/appliances/?v=6848ae6f8e78",
            #"referer": "https://frankotrading.com/product-category/printers/?v=6848ae6f8e78",
            "sec-ch-ua": '"Not=A?Brand";v="99", "Chromium";v="118"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        }
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            headers=self.headers,
            cookies=self.cookies,
        )

    def parse(self, response):
        # The initial product list parsing remains the same, but with added callback to parse_product
        products = response.css('li.product')
        for product in products:
            product_data = {
                'title': product.css('h2.woocommerce-loop-product__title a::text').get(),
                'price': product.css('span.woocommerce-Price-amount.amount::text').get(),
                'url': product.css('div.product-loop-image-wrapper a::attr("href")').get(),
                'photo': product.css('img.attachment-woocommerce_thumbnail::attr("src")').get()
            }
            # We yield a request to the product details page, passing along the collected product_data
            yield response.follow(
                product_data['url'],
                callback=self.parse_product,
                meta={'product_data': product_data}
            )

        next_page_url = response.css('a.next.page-numbers::attr(href)').get()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_product(self, response):


        # Get the passed product data from the previous method
        product_data = response.meta['product_data']
    
        # Scraping additional images from 'thumbnail-item' class
        thumbnail_images = response.css('div.thumbnail-item img::attr(src)').getall()

        # Remove duplicates by converting the list to a set and back to a list
        thumbnail_images = list(set(thumbnail_images))
        product_data['all_images'] = thumbnail_images

        # Scraping the details
        details = response.css('div#tab-description p::text').getall()
        product_data['details'] = details

        # Now we yield the final product data which includes details and images
        yield product_data






#### RUN BLOCK --- FOR YOUR BANNERS ONLY ------- #####

# class FrankoTradingImageSpider(scrapy.Spider):
#     name = 'frankotrading'
#     allowed_domains = ['frankotrading.com']
#     start_urls = ['https://frankotrading.com/?v=6848ae6f8e78']

#     def parse(self, response):
#         # Extract image URLs from 'data-lazyload' attribute in rs-slide elements
#         image_urls = response.css('rs-slide[data-lazyload]::attr(data-lazyload)').getall()
#         # Extract image URLs from 'img' tags
#         image_urls.extend(response.css('img::attr(src)').getall())
#         # Normalize the URLs and filter out any that are empty strings
#         image_urls = [response.urljoin(url) for url in image_urls if url.strip()]
#         # Return the items
#         return {'image_urls': image_urls}






###### TO RUN ANY CRAWL #######
# scrapy crawl {spidername} -o ../data/{spidername}/{category}.json
# Eg: scrapy crawl frankotrading -o ../data/frankotrading/appliances.json