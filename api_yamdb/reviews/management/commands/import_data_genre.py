import csv

from django.core.management import BaseCommand

from reviews.models import Genres


class Command(BaseCommand):
    help = 'Imports data from a CSV file into Genres'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str,
                            help='The path to the CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Genres.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
        self.stdout.write(
            self.style.SUCCESS('Data genre.csv imported successfully')
        )
