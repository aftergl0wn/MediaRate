import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Categories, Genres, Titles


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        DIR_DATA = settings.BASE_DIR / 'static' / 'data'
        file_path = DIR_DATA / 'category.csv'
        csv_file = kwargs[file_path]
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Categories.objects.create(
                    id=row['0'],
                    name=row['1'],
                    slug=row['2']
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))

        # csv_file = kwargs['comments.csv']
        # with open(csv_file, 'r') as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         Comment.objects.create(
        #             id=row['0'],
        #             review_id=row['1'],
        #             text=row['2'],
        #             author=row['3'],
        #             pub_date=row['4'],
        #         )
        # self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        # csv_file = kwargs['genre.csv']
        # with open(csv_file, 'r') as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         Categories.objects.create(
        #             id=row['0'],
        #             name=row['1'],
        #             slug=row['2']
        #         )
        # self.stdout.write(self.style.SUCCESS('Data imported successfully'))

        # csv_file = kwargs['genre_title.csv']
        # with open(csv_file, 'r') as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         Titles.objects.create(
        #             id=row['0'],
        #             title_id=row['1'],
        #         )
        #         Genres.objects.create(
        #             genre_id=row['2'],
        #         )
        # self.stdout.write(self.style.SUCCESS('Data imported successfully'))

        # csv_file = kwargs['review.csv']
        # with open(csv_file, 'r') as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         Review.objects.create(
        #             id=row['0'],
        #             title_id=row['1'],
        #             text=row['2'],
        #             author=row['3'],
        #             score=row['4'],
        #             pub_date=row['5'],
        #         )
        # self.stdout.write(self.style.SUCCESS('Data imported successfully'))

        # csv_file = kwargs['titles.csv']
        # with open(csv_file, 'r') as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         Titles.objects.create(
        #             id=row['0'],
        #             name=row['1'],
        #             year=row['2'],
        #             category=row['3'],
        #         )
        # self.stdout.write(self.style.SUCCESS('Data imported successfully'))

        # csv_file = kwargs['users.csv']
        # with open(csv_file, 'r') as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         Users.objects.create(
        #             id=row['0'],
        #             username=row['1'],
        #             email=row['2'],
        #             role=row['3'],
        #             score=row['4'],
        #             bio=row['5'],
        #             first_name=row['6'],
        #             last_name=row['7'],
        #         )
        # self.stdout.write(self.style.SUCCESS('Data imported successfully'))
