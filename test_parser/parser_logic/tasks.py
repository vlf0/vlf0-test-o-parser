from .parser_logic import OzonHTMLParser
from celery import shared_task
# from tg_bot.main import send_notification


@shared_task
def parse(product_amount):
    parser = OzonHTMLParser(product_amount)
    parser.save_to_db()
    # send_notification()
