# Generated by Django 3.2 on 2023-10-25 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Проверочный код'),
        ),
    ]
