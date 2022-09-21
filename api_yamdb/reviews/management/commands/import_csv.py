import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from ._csv_processing import CSVtoSQLite


class Command(BaseCommand):
    help = 'Import data from CSV to DataBase.'

    def add_arguments(self, parser):
        parser.add_argument("dir_path", type=str)

    def get_full_path(self, dir_path):
        return os.path.join(settings.BASE_DIR, dir_path)

    def handle(self, *args, **options):
        try:
            path_to_csv = self.get_full_path(options.get('dir_path'))
            csv_work = CSVtoSQLite(path_to_csv)
            self.stdout.write(
                'Found this csv files in folder:\n'
                f'{csv_work.csv_files}\n \n'
                f'This files will be imported to {csv_work.sqlite_db_name}:\n'
                f'{csv_work.csv_to_process}\n \n'
            )
        except FileNotFoundError as error:
            raise CommandError(error)
        try:
            csv_work.process_csv()
        except FileNotFoundError as error:
            raise CommandError(error)
