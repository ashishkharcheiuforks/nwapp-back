# Generated by Django 2.2.7 on 2019-12-22 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0004_comment_membercomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='membercomment',
            name='slug',
            field=models.SlugField(default=1, help_text='The unique identifier used externally.', max_length=255, unique=True, verbose_name='Slug'),
            preserve_default=False,
        ),
    ]