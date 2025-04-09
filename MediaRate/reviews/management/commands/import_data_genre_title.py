import csv

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Genres, GenreTitle, Title


class Command(BaseCommand):
    help = 'Imports data from a CSV file into GenreTitle'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str,
                            help='The path to the CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                GenreTitle.objects.create(
                    id=row['id'],
                    genre_id=get_object_or_404(Genres, id=row['genre_id']).id,
                    title_id=get_object_or_404(Title, id=row['title_id']).id,
                )
        self.stdout.write(
            self.style.SUCCESS('Data genre_title.csv imported successfully')
        )
