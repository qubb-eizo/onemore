# Generated by Django 3.1b1 on 2020-06-26 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsuite', '0002_auto_20200626_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresultdetails',
            name='text',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
    ]
