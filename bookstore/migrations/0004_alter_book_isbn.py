# Generated by Django 3.2.9 on 2021-12-20 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0003_alter_book_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(blank=True, default='3228111107375', max_length=13, null=True, unique=True),
        ),
    ]
