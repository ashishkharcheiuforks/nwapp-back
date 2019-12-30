# Generated by Django 2.2.7 on 2019-12-23 03:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import nwapp.s3utils
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tenant_foundation', '0005_membercomment_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateImageUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', sorl.thumbnail.fields.ImageField(help_text='The upload image.', storage=nwapp.s3utils.PrivateMediaStorage(), upload_to='uploads/%Y/%m/%d/')),
                ('is_archived', models.BooleanField(blank=True, db_index=True, default=False, help_text='Indicates whether private image was archived.', verbose_name='Is Archived')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('created_from', models.GenericIPAddressField(blank=True, help_text='The IP address of the creator.', null=True, verbose_name='Created from')),
                ('created_from_is_public', models.BooleanField(blank=True, default=False, help_text='Is creator a public IP and is routable.', verbose_name='Is the IP ')),
                ('last_modified_at', models.DateTimeField(auto_now=True)),
                ('last_modified_from', models.GenericIPAddressField(blank=True, help_text='The IP address of the modifier.', null=True, verbose_name='Last modified from')),
                ('last_modified_from_is_public', models.BooleanField(blank=True, default=False, help_text='Is modifier a public IP and is routable.', verbose_name='Is the IP ')),
                ('created_by', models.ForeignKey(blank=True, help_text='The user whom created this image.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_private_image_uploads', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(blank=True, help_text='The user whom last modified this private image upload.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_modified_private_image_uploads', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(help_text='The user whom this belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='private_image_uploads', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Private Image Upload',
                'verbose_name_plural': 'Private Image Uploads',
                'db_table': 'nwapp_private_image_uploads',
                'permissions': (),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='PrivateFileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_file', models.FileField(help_text='The upload binary file.', storage=nwapp.s3utils.PrivateMediaStorage(), upload_to='uploads/%Y/%m/%d/')),
                ('title', models.CharField(blank=True, help_text='The tile content of this upload.', max_length=63, null=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, help_text='The text content of this upload.', null=True, verbose_name='Description')),
                ('is_archived', models.BooleanField(blank=True, db_index=True, default=False, help_text='Indicates whether private file was archived.', verbose_name='Is Archived')),
                ('indexed_text', models.CharField(blank=True, db_index=True, help_text='The searchable content text used by the keyword searcher function.', max_length=511, null=True, unique=True, verbose_name='Indexed Text')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('created_from', models.GenericIPAddressField(blank=True, help_text='The IP address of the creator.', null=True, verbose_name='Created from')),
                ('created_from_is_public', models.BooleanField(blank=True, default=False, help_text='Is creator a public IP and is routable.', verbose_name='Is the IP ')),
                ('last_modified_at', models.DateTimeField(auto_now=True)),
                ('last_modified_from', models.GenericIPAddressField(blank=True, help_text='The IP address of the modifier.', null=True, verbose_name='Last modified from')),
                ('last_modified_from_is_public', models.BooleanField(blank=True, default=False, help_text='Is modifier a public IP and is routable.', verbose_name='Is the IP ')),
                ('created_by', models.ForeignKey(blank=True, help_text='The user whom created this file.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_private_file_uploads', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(blank=True, help_text='The user whom last modified this private file upload.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_modified_private_file_uploads', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, help_text='The tags associated with this private file uploads.', related_name='private_file_uploads', to='tenant_foundation.Tag')),
                ('user', models.ForeignKey(help_text='The user whom this belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='private_file_uploads', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Private File Upload',
                'verbose_name_plural': 'Private File Uploads',
                'db_table': 'nwapp_private_file_uploads',
                'permissions': (),
                'default_permissions': (),
            },
        ),
    ]