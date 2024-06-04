# -*- coding: utf-8 -*-
from typing import Union
from .serializers import ParsingSerializer
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import bs4


class OzonHTMLParser:

    def __init__(self, shop_url: str, obj_amount: int) -> None:
        """
        Initialize an instance of Ozon parser.

        :param shop_url: The full URL of chosen shop in Ozon.ru.
        :param obj_amount: Amount of products what you want to parse.
        """
        self.obj_amount = obj_amount
        self.default_page_amount = 36
        self.reminded_obj_amount = None
        self.pages_contents = []
        self.page_number = 2
        self.shop_url = shop_url
        self.partial_href = self.get_partial_href()
        self.antibot_link = shop_url + '&__rr=1'
        self.parsed_objects = []
        self.product_links = []
        self.descriptions = []

    @staticmethod
    def get_tag(content: str, name: str, **kwargs) -> bs4.element.Tag:
        """
        Extracts a specific HTML tag from the given content.

        :param content: The HTML content to parse.
        :param name: The name of the tag to extract.
        :param kwargs: Additional arguments for tag attributes.
        :return: The first matching tag or None if no tag is found.
        """
        soup = BeautifulSoup(content, 'html.parser')
        tag = soup.find(name, **kwargs) if kwargs else soup.find(name)
        return tag

    def get_partial_href(self) -> str:
        """
        Derives the partial URL from the shop URL.

        :return: The partial URL string.
        """
        return self.shop_url.split('ru')[1]

    def get_pages_content(self, browser_obj) -> None:
        """
        Retrieves the content of the pages to be parsed.

        :param browser_obj: The browser instance from Playwright.
        """
        pages_amount = self.obj_amount // self.default_page_amount
        pages = range(pages_amount + 1)
        self.reminded_obj_amount = (self.obj_amount - pages_amount * self.default_page_amount)
        context = browser_obj.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                                     ' (KHTML, like Gecko) Chrome/91.0.4272.124 Safari/537.36')
        page = context.new_page()
        page.set_default_timeout(60000)

        for page_number in pages:
            if pages.index(page_number) == 0:
                page.goto(self.shop_url)
                page.wait_for_load_state()
                if page.url == self.antibot_link:
                    try:
                        page.locator('#reload-button').click()
                        page.wait_for_load_state()
                        self.pages_contents.append(page.content())
                    except Exception:
                        browser_obj.close()
                        return
            else:
                page.locator(f'a[href="{self.partial_href}&page={self.page_number}"]',
                             has_text='Дальше'
                             ).click()
                page.wait_for_load_state()
                self.page_number += 1
                page_content = page.content()
                self.pages_contents.append(page_content)

    def parse_it(self) -> None:
        """
        Main method to parse the pages content and extract product information.

        Parsed products data will save in class object attribute "parsed_objects".
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)

            self.get_pages_content(browser)
            browser.close()

            amount = self.default_page_amount
            for content in self.pages_contents:
                ozon_tag = self.get_tag(content, 'div', id='__ozon')
                shop_container = ozon_tag.footer.previous_sibling
                products_column = shop_container.next.next.next.next_sibling.next.next_sibling.next_sibling.next
                products_widget = products_column.next.next.next.next
                products_tags = [tag for tag in products_widget if isinstance(tag, bs4.element.Tag)]
                if self.pages_contents.index(content) + 1 == len(self.pages_contents):
                    amount = self.reminded_obj_amount
                self.create_products_list(products_tags, amount)

    def create_products_list(self, tags: Union[list, bs4.element.Tag], amount: int) -> None:
        """
        Add to self attribute a list of product information from the parsed HTML tags of one page.

        :param tags: The HTML tags containing product information.
        :param amount: The number of products to parse from the tags.
        """
        for child in tags[:amount]:
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

    def save_to_db(self):
        """
        Parses the product information and saves it to the database.
        # """
        self.parse_it()
        for product in self.parsed_objects:
            serializer = ParsingSerializer(data=product)
            if serializer.is_valid():
                serializer.save()



