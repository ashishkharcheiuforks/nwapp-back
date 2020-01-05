# Generated by Django 2.2.7 on 2020-01-05 04:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tenant_foundation', '0008_badge_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssociateAddress',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('tenant_foundation.memberaddress',),
        ),
        migrations.CreateModel(
            name='AssociateContact',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('tenant_foundation.membercontact',),
        ),
        migrations.CreateModel(
            name='AssociateMetric',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('tenant_foundation.membermetric',),
        ),
        migrations.AlterModelOptions(
            name='associate',
            options={'default_permissions': (), 'permissions': (), 'verbose_name': 'Associate', 'verbose_name_plural': 'Associates'},
        ),
        migrations.RemoveField(
            model_name='associate',
            name='member',
        ),
        migrations.AddField(
            model_name='associate',
            name='user',
            field=models.OneToOneField(default=1, help_text='The user whom is an associate.', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='associate', serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AssociateComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='The unique identifier used externally.', max_length=255, unique=True, verbose_name='Slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('associate', models.ForeignKey(help_text='The area coordinator whom this comment is about.', on_delete=django.db.models.deletion.CASCADE, related_name='associate_comments', to='tenant_foundation.Associate')),
                ('comment', models.ForeignKey(help_text='The comment this item belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='area_associates', to='tenant_foundation.Comment')),
            ],
            options={
                'verbose_name': 'Associate Comment',
                'verbose_name_plural': 'Associate Comments',
                'db_table': 'nwapp_associate_comments',
                'ordering': ['-created_at'],
                'permissions': (),
                'default_permissions': (),
            },
        ),
    ]