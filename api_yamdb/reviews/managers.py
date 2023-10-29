from django.db import models


class TitleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            rating=models.Avg('reviews__score')
        )
