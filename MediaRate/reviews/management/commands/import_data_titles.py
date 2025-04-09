import csv

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Categories, Title


class Command(BaseCommand):
    help = 'Imports data from a CSV file into Title'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str,
                            help='The path to the CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=get_object_or_404(Categories, id=row['category']),
                )
        self.stdout.write(
            self.style.SUCCESS('Data titles.csv imported successfully')
        )
