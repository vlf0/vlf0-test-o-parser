import httpx
from .parser_logic import OzonHTMLParser
from celery import shared_task


@shared_task(max_retries=3)
def parse(product_amount):
    try:
        parser = OzonHTMLParser(product_amount)
        parser.save_to_db()
        response = httpx.post(f"http://bot:9000/send-notification/", json={"product_amount": product_amount})
        response.raise_for_status()
        return True
    except Exception as e:
        parse.retry(exc=e, countdown=10)

