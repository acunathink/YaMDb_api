import csv
from django.core.management.base import BaseCommand
from reviews.models import User, Title, Category, Genre, Review, Comment


CSV = {
    User: 'users.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Genre: 'genre.csv',
    Review: 'review.csv',
    Comment: 'comments.csv'
}


class Command(BaseCommand):
    help = 'Command for import csv files'

    def handle(self, *args, **options):
        for model, file in CSV.items():
            with open(f'static/data/{file}', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                if model.objects.exists():
                    self.stdout.write(self.style.WARNING(
                        f'Для модели "{model._meta.verbose_name}" '
                        f'данные уже добавлены!'))
                    continue
                model.objects.bulk_create(
                    model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Все данные импортированы'))