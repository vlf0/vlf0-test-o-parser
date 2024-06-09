from django.core.management.base import BaseCommand
import time
import MySQLdb
from django.conf import settings


class Command(BaseCommand):

    has_data = False

    def handle(self, *args, **kwargs):
        while not self.has_data:
            time.sleep(5)
            self.stdout.write(self.style.WARNING('Database is not initialized yet. Retry after 5 sec...'))
            self.has_data_in_database()
        self.stdout.write(self.style.SUCCESS('Database initialization checking success.'))

    def has_data_in_database(self):
        db_settings = settings.DATABASES['default']
        try:
            connection = MySQLdb.connect(
                host=db_settings['HOST'],
                user=db_settings['USER'],
                password=db_settings['PASSWORD'],
                database=db_settings['NAME'],
                port=int(db_settings['PORT']) if db_settings['PORT'] else 3306
            )
            cursor = connection.cursor()
            cursor.execute(f"USE parsing;")
            self.has_data = True
        except MySQLdb.Error as e:
            self.stdout.write(self.style.ERROR('not ready'))

