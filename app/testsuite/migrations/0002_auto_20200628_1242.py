# Generated by Django 3.1b1 on 2020-06-28 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsuite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='text',
            field=models.CharField(max_length=1024),
        ),
    ]
