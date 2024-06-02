# -*- coding: utf-8 -*-
from .serializers import ParsingSerializer
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import bs4
import time


class OzonHTMLParser:

    def __init__(self, obj_amount):
        self.obj_amount = obj_amount
        self.url = 'https://www.ozon.ru/seller/proffi-1/products/?miniapp=seller_1'
        self.antibot_link = self.url + '&__rr=1'
        self.parsed_objects = []
        self.product_links = []
        self.descriptions = []
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/91.0.4472.124 Safari/537.36",

            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)"
            " Version/14.0.3 Safari/605.1.15",

            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        ]

    @staticmethod
    def get_tag(content, name, **kwargs):
        soup = BeautifulSoup(content, 'html.parser')
        tag = soup.find(name, **kwargs) if kwargs else soup.find(name)
        return tag

    def parse_it(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                                                     " (KHTML, like Gecko) Chrome/91.0.4272.124 Safari/537.36")
            page = context.new_page()
            page.set_default_timeout(90000)

            page.goto(self.url)
            time.sleep(2)
            if page.url == self.antibot_link:
                selector = '#reload-button'
                try:
                    page.click(selector)
                    time.sleep(3)
                    page.wait_for_load_state()
                except Exception as e:
                    print(f"Error clicking reload button: {e}")
                    browser.close()
                    return

            content = page.content()
            browser.close()

            ozon_tag = self.get_tag(content, 'div', id='__ozon')
            shop_container = ozon_tag.footer.previous_sibling
            products_column = shop_container.next.next.next.next_sibling.next.next_sibling.next_sibling.next
            products_widget = products_column.next.next.next.next

            products_tags = [tag for tag in products_widget if isinstance(tag, bs4.element.Tag)]

            for child in products_tags[:self.obj_amount]:
                product_text = child.a.next_sibling.next_sibling
                cost = (product_text.div.div.span.string.replace('\u2009', '')).rstrip('₽')
                discount = (product_text.div.div.span.next_sibling.next_sibling.get_text()).lstrip('−')
                name = product_text.a.string
                img_link = child.img['src']
                self.product_links.append(child.a['href'])
                parsed_product = {'name': name,
                                  'price': cost,
                                  'description': 'default',
                                  'image_url': img_link,
                                  'discount': discount}
                self.parsed_objects.append(parsed_product)
        return self.parsed_objects

    def save_to_db(self):
        parsed_data = self.parse_it()
        for product in parsed_data:
            serializer = ParsingSerializer(data=product)
            if serializer.is_valid():
                serializer.save()

