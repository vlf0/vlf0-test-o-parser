# -*- coding: utf-8 -*-
from typing import Union
from .serializers import BaseParsingSerializer
from playwright.sync_api import sync_playwright
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import bs4


def smooth_scroll(page, scroll_to: int, duration: int):
    """
    Performs a smooth scroll to a specific position on the page.

    :param page: The Playwright page object.
    :param scroll_to: The position to scroll to.
    :param duration: The duration of the scroll in milliseconds.
    """
    scroll_script = f"""
        const scrollTo = {scroll_to};
        const duration = {duration};
        const step = scrollTo / (duration / 16);
        function scroll() {{
            const top = window.scrollY;
            if (top < scrollTo) {{
                window.scrollBy(0, step);
                setTimeout(scroll, 16);
            }} else {{
                window.scrollTo(0, scrollTo);
            }}
        }}
        scroll();
        """
    page.evaluate(scroll_script)


class OzonHTMLParser:

    def __init__(self, obj_amount: int) -> None:
        """
        Initialize an instance of Ozon parser.

        :param obj_amount: Amount of products what you want to parse.
        """
        self.obj_amount = obj_amount
        self.default_page_amount = 36
        self.pages_amount = self.get_pages_amount()
        self.reminded_obj_amount = None
        self.pages_contents = []
        self.page_number = 2
        self.shop_url = 'https://www.ozon.ru/seller/proffi-1/products/?miniapp=seller_1'
        self.partial_href = self.get_partial_href()
        self.antibot_link = self.shop_url + '&__rr=1'
        self.main_dict = []
        self.product_links = []
        self.descriptions = []
        self.text_descriptions = []
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
                          ' (KHTML, like Gecko) Chrome/91.0.4272.124 Safari/537.36'

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

    @staticmethod
    def get_browser(parsing_branch):
        """
        Launches a new browser instance and performs parsing operations.

        :param parsing_branch: A function representing the parsing logic.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            parsing_branch(browser)
            browser.close()

    def create_page(self, browser_obj):
        """
        Creates a new page within the browser context.

        :param browser_obj: The browser instance.
        :return: The newly created page.
        """
        context = browser_obj.new_context(user_agent=self.user_agent)
        page = context.new_page()
        return page

    @staticmethod
    def get_products_container(page):
        """
        Waits for the products container to be loaded and scrolls to the bottom of the page.

        :param page: The Playwright page object.
        """
        page.wait_for_load_state('load')
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        paginator = page.locator('div[id="paginatorContent"]')
        paginator.wait_for()

    @staticmethod
    def get_description_container(page):
        """
        Waits for the description container to be loaded, scrolls to the bottom of the page,
        and ensures the description section is attached.

        :param page: The Playwright page object.
        """
        page.wait_for_load_state('load')
        page_height = page.evaluate('document.body.scrollHeight')
        smooth_scroll(page, page_height, 2500)
        paginator = page.locator('div#section-description').nth(0)
        paginator.wait_for(timeout=70000)

    def get_partial_href(self) -> str:
        """
        Derives the partial URL from the shop URL.

        :return: The partial URL string.
        """
        return self.shop_url.split('ru')[1]

    def get_pages_amount(self) -> int:
        """
        Calculates the total number of pages to parse.

        :return: The number of pages.
        """
        return self.obj_amount // self.default_page_amount

    def get_pages_content(self, browser_obj) -> None:
        """
        Retrieves the common content of the pages to be parsed from grid widget.

        :param browser_obj: The browser instance from Playwright.
        """
        pages = range(self.pages_amount + 1)
        self.reminded_obj_amount = (self.obj_amount - self.pages_amount * self.default_page_amount)
        page = self.create_page(browser_obj)
        page_num = 2
        for page_number in pages:
            if pages.index(page_number) == 0:
                page.goto(self.shop_url)
                if page.url == self.antibot_link:
                    try:
                        reload_btn = page.get_by_role('button', name='Обновить')
                        reload_btn.wait_for()
                        reload_btn.click()
                    except Exception:
                        browser_obj.close()
                        return
                self.get_products_container(page)
                self.pages_contents.append(page.content())
            else:
                page.locator(f'a[href="{self.partial_href}&page={page_num}"]',
                             has_text='Дальше'
                             ).click()
                self.get_products_container(page)
                page_num += 1
                page_content = page.content()
                self.pages_contents.append(page_content)

    def get_detail_pages_content(self, browser_obj):
        """
        Retrieves detailed content of individual product pages.

        :param browser_obj: The browser instance from Playwright.
        """
        page = self.create_page(browser_obj)
        page.goto(self.shop_url)
        page.wait_for_load_state('domcontentloaded')

        if page.url == self.antibot_link:
            try:
                page.locator('#reload-button').click()
                page.wait_for_load_state('domcontentloaded')
            except Exception:
                browser_obj.close()
                return

        for link in self.product_links:
            page.goto(f'https://ozon.ru{link}')
            self.get_description_container(page)
            content = page.content()
            self.descriptions.append(content)

    def parse_main_part(self):
        """
        Parses the main content of product listing pages with "description" field "default" values
        and save it to self attribute as list.
        """
        amount = self.default_page_amount
        for content in self.pages_contents:
            products_container = self.get_tag(content, 'div', id='paginatorContent')
            products_widget = products_container.div.div
            products_tags = [tag for tag in products_widget if isinstance(tag, bs4.element.Tag)
                             and 'tile-root' in tag['class']]

            # while len(products_tags) != self.default_page_amount:
            #     self.pages_contents = []
            #     self.get_browser(self.get_pages_content)
            #     self.parse_main_part()

            if self.pages_contents.index(content) + 1 == len(self.pages_contents):
                amount = self.reminded_obj_amount
            self.create_products_list(products_tags, amount)

    def parse_descriptions(self):
        """Extracts and stores text descriptions of products in the self attr."""
        for page_content in self.descriptions:
            soup = BeautifulSoup(page_content, 'html.parser')
            section_description = soup.find('div', id='section-description')
            description = section_description.next_element.next_sibling.next_element.get_text()
            self.text_descriptions.append(description.strip())

    def add_descriptions(self) -> None:
        """Adds descriptions to the main product dictionary creating full ready data that was parsed."""
        for product_dict, description in zip(self.main_dict, self.text_descriptions):
            product_dict['description'] = description

    def parse_it(self) -> None:
        """
        Main method to parse the pages content and extract product information.

        After parsing is merging main dict and descriptions alongside.
        This dict will save in class object attribute "parsed_objects".
        """
        with Display(backend="xvfb", size=(100, 60)):
            self.get_browser(self.get_pages_content)
            self.parse_main_part()
            self.get_browser(self.get_detail_pages_content)
            self.parse_descriptions()
            self.add_descriptions()

    def create_products_list(self, tags: Union[list, bs4.element.Tag], amount: int) -> None:
        """
        Add to self attribute a list of product information from the parsed HTML tags of one page.

        :param tags: The HTML tags containing product information.
        :param amount: The number of products to parse from the tags.
        """
        for child in tags[:amount]:
            product_text = child.div.a.next_sibling.next_sibling
            cost = (product_text.span.string.replace('\u2009', '')).rstrip('₽')
            discount = (product_text.span.next_sibling.next_sibling.get_text()).lstrip('−')
            name = product_text.a.string
            img_link = child.img['src']
            product_link = child.a['href']
            parsed_product = {'name': name,
                              'price': cost,
                              'description': 'default',
                              'image_url': img_link,
                              'discount': discount,
                              'link': 'https://www.ozon.ru' + product_link}
            self.product_links.append(product_link)
            self.main_dict.append(parsed_product)

    def save_to_db(self):
        """
        Parses the product information and saves it to the database.
        """
        self.parse_it()
        for product in self.main_dict:
            serializer = BaseParsingSerializer(data=product)
            if serializer.is_valid(raise_exception=True):
                serializer.save()


if __name__ == '__main__':
    parser = OzonHTMLParser(15)
    parser.parse_it()
