# Generated by Django 3.2.9 on 2021-12-10 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(blank=True, default='6920667022247', max_length=13, null=True, unique=True),
        ),
    ]
