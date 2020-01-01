# Generated by Django 2.2.7 on 2020-01-01 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_foundation', '0002_auto_20191222_0213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareduser',
            name='tos_signed_on',
            field=models.DateTimeField(blank=True, help_text='The date when the service agreement was signed on.', null=True, verbose_name='Terms of service signed on'),
        ),
    ]
