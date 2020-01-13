# Generated by Django 2.2.7 on 2020-01-13 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tenant_foundation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of', models.PositiveSmallIntegerField(choices=[(1, 'Residential'), (2, 'Business'), (3, 'Community Cares')], db_index=True, help_text='The type of score point this is.', verbose_name='Type of')),
                ('name', models.CharField(db_index=True, help_text='The name of this district.', max_length=127, unique=True, verbose_name='Name')),
                ('description', models.CharField(blank=True, help_text='The description of this district.', max_length=255, null=True, verbose_name='Description')),
                ('counselor_name', models.CharField(blank=True, help_text="The name of this district's counselor.", max_length=127, null=True, verbose_name='Counselor Name')),
                ('counselor_email', models.EmailField(blank=True, help_text="The email of this district's counselor.", max_length=127, null=True, verbose_name='Counselor Email')),
                ('counselor_phone', models.CharField(blank=True, help_text="The phone of this district's counselor.", max_length=127, null=True, verbose_name='Counselor Phone')),
                ('website_url', models.URLField(blank=True, help_text='The external website link of this district.', max_length=255, null=True, verbose_name='Website URL')),
                ('slug', models.SlugField(help_text='The unique identifier used externally.', max_length=255, unique=True, verbose_name='Slug')),
                ('is_archived', models.BooleanField(blank=True, db_index=True, default=False, help_text='Indicates whether district was archived or not', verbose_name='Is Archived')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('created_from', models.GenericIPAddressField(blank=True, help_text='The IP address of the creator.', null=True, verbose_name='Created from')),
                ('created_from_is_public', models.BooleanField(blank=True, default=False, help_text='Is creator a public IP and is routable.', verbose_name='Is the IP ')),
                ('last_modified_at', models.DateTimeField(auto_now=True)),
                ('last_modified_from', models.GenericIPAddressField(blank=True, help_text='The IP address of the modifier.', null=True, verbose_name='Last modified from')),
                ('last_modified_from_is_public', models.BooleanField(blank=True, default=False, help_text='Is modifier a public IP and is routable.', verbose_name='Is the IP ')),
                ('created_by', models.ForeignKey(blank=True, help_text='The user whom created this score point.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_districts', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(blank=True, help_text='The user whom last modified this private image upload.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_modified_districts', to=settings.AUTH_USER_MODEL)),
                ('logo_image', models.ForeignKey(blank=True, help_text='The logo image of this district.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='districts', to='tenant_foundation.PrivateImageUpload')),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
                'db_table': 'nwapp_districts',
                'permissions': (),
                'default_permissions': (),
            },
        ),
    ]
