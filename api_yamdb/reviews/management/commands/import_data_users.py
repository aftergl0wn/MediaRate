import csv

from django.core.management import BaseCommand

from reviews.models import User


class Command(BaseCommand):
    help = 'Imports data from a CSV file into User'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str,
                            help='The path to the CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                User.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
        self.stdout.write(
            self.style.SUCCESS('Data users.csv imported successfully')
        )
