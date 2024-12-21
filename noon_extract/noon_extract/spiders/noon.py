import scrapy
from datetime import datetime
import re


class NoonSpider(scrapy.Spider):
    name = "noon"
    allowed_domains = ["noon.com"]
    start_urls = ["https://www.noon.com/uae-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/"]

    custom_settings = {
        'DOWNLOAD_DELAY': 0.25,
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'noon_products.csv',
        'CONCURRENT_REQUESTS': 8,
        'RETRY_TIMES': 5,
    }

    def parse(self, response):
        products = response.css(".productContainer")
        
        for product in products:
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sku = product.css("a::attr(href)").re_first(r"/([A-Z0-9]+)[/p]")
            product_name = product.css('[data-qa="product-name"]::attr(title)').get()
            brand = "sc-f35b8612-21 ovuGP"
            rating = product.css("div[class*='dGLdNc']::text").get() or "NA"
            rating_count = product.css("span[class*='DkxLK']::text").get() or "NA"
            sponsored = "Y" if product.css("div[class*='gzboVs']::text").get() else "N"
            price = product.css(".oldPrice::text").get() or "aaa"
            sales_price = product.css("strong[class='amount']::text").get()
            express_img_srcs = product.css("img::attr(src)").getall()
            express_delivery = (
                "Y" if "https://f.nooncdn.com/s/app/com/noon/images/fulfilment_express_v3-en.svg" in express_img_srcs else "N"
            )
            rank = ""
            link = "https://www.noon.com" + product.css("a::attr(href)").get()
            print("\n", price,"aaaaaaaaaaaaaaaaaaaaaa\n")
            yield {
                "Date & Time": date_time,
                "SKU": sku,
                "Name": product_name,
                "Brand": brand,
                "Average Rating": rating,
                "Rating Count": rating_count,
                "Sponsered": sponsored,
                "Price": price,
                "Sales Price": sales_price,
                "Express": express_delivery,
                "Rank": rank,
                "Link": link,
            }

        next_page = response.css("a.nextPage::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
