import scrapy
from datetime import datetime


class NoonSpider(scrapy.Spider):
    name = "noon"
    allowed_domains = ["noon.com"]
    start_urls = ["https://www.noon.com/uae-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/?limit=500"]

    custom_settings = {
        'DOWNLOAD_DELAY': 0.25,
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'noon_products.csv',
        'CONCURRENT_REQUESTS': 8,
        'RETRY_TIMES': 5,
        'FEED_EXPORT_FIELDS': [
            "Date & Time", "SKU", "Name", "Brand", "Average Rating", "Rating Count", "Sponsered", 
            "Price", "Sales Price", "Express", "Rank", "Link"
        ],
    }
    rank_counter = 1

    def parse(self, response):
        products = response.css(".productContainer")
        for product in products:
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sku = product.css("a::attr(href)").re_first(r"/([A-Z0-9]+)[/p]")
            product_name = product.css('[data-qa="product-name"]::attr(title)').get()
            rating = product.css("div[class*='dGLdNc']::text").get() or "NA"
            rating_count = product.css("span[class*='DkxLK']::text").get() or "NA"
            sponsored = "Y" if product.css("div[class*='gzboVs']::text").get() else "N"
            price = product.css("span.oldPrice::text").get() or "NA"
            sales_price = product.css("strong[class='amount']::text").get()
            express_img_srcs = product.css("img::attr(src)").getall()
            express_delivery = (
                "Y" if "https://f.nooncdn.com/s/app/com/noon/images/fulfilment_express_v3-en.svg" in express_img_srcs else "N"
            )
            link = "https://www.noon.com" + product.css("a::attr(href)").get()

            rank = self.rank_counter
            self.rank_counter += 1

            request = response.follow(
                link,
                callback=self.parse_product_detail,
                meta={
                    "Date & Time": date_time,
                    "SKU": sku,
                    "Name": product_name,
                    "Average Rating": rating,
                    "Rating Count": rating_count,
                    "Sponsered": sponsored,
                    "Price": price,
                    "Sales Price": sales_price,
                    "Express": express_delivery,
                    "Rank": rank,
                    "Link": link,
                },
            )
            yield request

    def parse_product_detail(self, response):
        brand = response.css("div.sc-f35b8612-21.ovuGP::text").get() or "NA"
        meta_data = response.meta
        meta_data["Brand"] = brand
        yield {
            "Date & Time": meta_data["Date & Time"],
            "SKU": meta_data["SKU"],
            "Name": meta_data["Name"],
            "Brand": meta_data["Brand"],
            "Average Rating": meta_data["Average Rating"],
            "Rating Count": meta_data["Rating Count"],
            "Sponsered": meta_data["Sponsered"],
            "Price": meta_data["Price"],
            "Sales Price": meta_data["Sales Price"],
            "Express": meta_data["Express"],
            "Rank": meta_data["Rank"],
            "Link": meta_data["Link"],
        }
