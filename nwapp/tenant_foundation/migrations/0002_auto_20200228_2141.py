# Generated by Django 2.2.7 on 2020-02-28 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='privateimageupload',
            name='title',
            field=models.CharField(blank=True, help_text='The image title of this upload.', max_length=63, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='privatefileupload',
            name='title',
            field=models.CharField(blank=True, help_text='The file title of this upload.', max_length=63, null=True, verbose_name='Title'),
        ),
    ]
