import csv

from django.core.management import BaseCommand

from reviews.models import Categories


class Command(BaseCommand):
    help = 'Imports data from a CSV file into Categories'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str,
                            help='The path to the CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Categories.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
        self.stdout.write(
            self.style.SUCCESS('Data category.csv imported successfully')
        )
