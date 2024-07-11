import csv

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Comment, Review, User


class Command(BaseCommand):
    help = 'Imports data from a CSV file into Comment'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str,
                            help='The path to the CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Comment.objects.create(
                    id=row['id'],
                    review_id=get_object_or_404(
                        Review, id=row['review_id']
                    ).id,
                    text=row['text'],
                    author=get_object_or_404(User, id=row['author']),
                    pub_date=row['pub_date'],
                )
        self.stdout.write(
            self.style.SUCCESS('Data comments.csv imported successfully')
        )
