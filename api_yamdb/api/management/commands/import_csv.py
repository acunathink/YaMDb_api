import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User

CSV = {
    User: 'users.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Genre: 'genre.csv',
    Review: 'review.csv',
    Comment: 'comments.csv'
}


class Command(BaseCommand):
    """Импорт csv-файлов."""
    help = 'Command for import csv files'

    def handle(self, *args, **options):
        for model, file in CSV.items():
            with open(f'static/data/{file}', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                if model.objects.exists():
                    self.stdout.write(self.style.WARNING(
                        f'Для модели "{model._meta.verbose_name}" '
                        f'данные уже добавлены!')
                    )
                    continue
                model.objects.bulk_create(
                    model(**data) for data in reader
                )

        with open('static/data/genre_title.csv', encoding='utf-8') as gt:
            reader = csv.DictReader(gt)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)

        self.stdout.write(self.style.SUCCESS('Все данные импортированы'))
