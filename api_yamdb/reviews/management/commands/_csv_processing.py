import csv
import os
import sqlite3

from django.core.management.base import CommandError
from django.utils import timezone


class CSVtoSQLite():
    """
    Class that provide interaction between SQLite and csv files.

    Expects for ags:
    - path to folder with csv files(required)
    - database name (optional)
    """

    def __init__(self,
                 path_to_csv,
                 sqlite_db_name=None):

        self.path_to_csv = path_to_csv
        if sqlite_db_name is None:
            sqlite_db_name = 'db.sqlite3'
        self.sqlite_db_name = sqlite_db_name
        self.csv_files = self.__get_csv_files()
        self.csv_to_process = list(self.__get_csv_to_process().keys())

    def __get_csv_files(self, file_ext=True):
        """Return list with csv files in foder."""
        files_list = os.listdir(self.path_to_csv)
        csv_files = []
        for file in files_list:
            if file.endswith('.csv'):
                if file_ext is True:
                    csv_files.append(file)
                if file_ext is False:
                    csv_files.append(file.split('.')[0])
        return csv_files

    def __get_csv_to_process(self):
        """Return dict with pars of csv file name and method to process csv."""
        csv_file_method = {}
        for method in dir(self):
            if method.startswith('import_') and method.endswith(
                tuple(self.__get_csv_files(file_ext=False))
            ):
                csv_file_method[method.split('import_')[1] + '.csv'] = method
        return csv_file_method

    def __do_job(self, import_method, csv_file_name):
        """Add data from csv to DB with specified method."""
        print(f'Importing from {csv_file_name} started.')
        start_time = timezone.now()
        try:
            connect = sqlite3.connect(self.sqlite_db_name)
            cursor = connect.cursor()
            with open(os.path.join(self.path_to_csv, csv_file_name), 'r',
                      newline='', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                next(reader)
                import_method(cursor, reader)
            end_time = timezone.now()
            print(f'Importing from {csv_file_name} done for '
                  f'{(end_time-start_time).total_seconds()} sec.\n \n')
            csv_file.close()
        except sqlite3.OperationalError as error:
            raise CommandError(error)
        finally:
            connect.commit()
            connect.close()

    def process_csv(self):
        """Run loop with __do_job() to process all csv files."""
        for csv_file_name, method in self.__get_csv_to_process().items():
            self.__do_job(getattr(self, method), csv_file_name)

    def import_users(self, cursor, reader):
        """Method for users processing."""
        for row in reader:
            try:
                cursor.execute('''
                INSERT INTO users_user
                (id,password,username,first_name,last_name,is_staff,email,bio,role,is_active,is_superuser)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                               (int(row[0]),
                                '',
                                str(row[1]),
                                str(row[5]),
                                str(row[6]),
                                (str(row[3]) == 'admin'
                                or str(row[3]) == 'moderator'),
                                str(row[2]),
                                str(row[4]),
                                str(row[3]),
                                '',
                                False))
            except sqlite3.IntegrityError:
                print(f'User {str(row[1])} exist.')

    def import_category(self, cursor, reader):
        """Method for category processing."""
        for row in reader:
            try:
                cursor.execute('''
                INSERT INTO reviews_categories
                (id,name,slug)
                VALUES (?,?,?)''',
                               (int(row[0]),
                                str(row[1]),
                                str(row[2])))
            except sqlite3.IntegrityError:
                print(f'Category {str(row[1])} exist.')

    def import_comments(self, cursor, reader):
        """Method for comments processing."""
        for row in reader:
            try:
                cursor.execute('''
                INSERT INTO reviews_comment
                (id,pub_date,text,author_id,review_id)
                VALUES (?,?,?,?,?)''',
                               (int(row[0]),
                                str(row[4]),
                                str(row[2]),
                                int(row[3]),
                                int(row[1])))
            except sqlite3.IntegrityError:
                print(f'Comments {str(row[2])} exist.')

    def import_genre_title(self, cursor, reader):
        """Method for genre_title processing."""
        for row in reader:
            try:
                cursor.execute('''
                INSERT INTO reviews_genretitle
                (id,genre_id,title_id)
                VALUES (?,?,?)''',
                               (int(row[0]),
                                str(row[2]),
                                str(row[1])))
            except sqlite3.IntegrityError:
                print(f'Genre_title {str(row[1])} exist.')

    def import_genre(self, cursor, reader):
        """Method for genre processing."""
        for row in reader:
            try:
                cursor.execute('''
                INSERT INTO reviews_genre
                (id,name,slug)
                VALUES (?,?,?)''',
                               (int(row[0]),
                                str(row[1]),
                                str(row[2])))
            except sqlite3.IntegrityError:
                print(f'Genre {str(row[1])} exist.')

    def import_review(self, cursor, reader):
        """Method for review processing."""
        for row in reader:
            try:
                cursor.execute('''
                INSERT INTO reviews_review
                (id,pub_date,text,score,author_id,title_id)
                VALUES (?,?,?,?,?,?)''',
                               (int(row[0]),
                                str(row[5]),
                                str(row[2]),
                                int(row[4]),
                                str(row[3]),
                                int(row[1])))
            except sqlite3.IntegrityError:
                print(f'Review {str(row[2])} exist.')

    def import_titles(self, cursor, reader):
        """Method for titles processing."""
        for row in reader:
            try:
                cursor.execute('''
                INSERT INTO reviews_title
                (id,name,year,category_id)
                VALUES (?,?,?,?)''',
                               (int(row[0]),
                                str(row[1]),
                                int(row[2]),
                                int(row[3])))
            except sqlite3.IntegrityError:
                print(f'Titles {str(row[1])} exist.')
