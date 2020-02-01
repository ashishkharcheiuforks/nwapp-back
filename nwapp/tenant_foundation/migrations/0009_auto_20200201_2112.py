# Generated by Django 2.2.7 on 2020-02-01 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0008_privatefileupload_watch'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatefileupload',
            name='district',
            field=models.ForeignKey(blank=True, help_text='The district whom this file belongs to.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='private_file_uploads', to='tenant_foundation.District'),
        ),
        migrations.AddField(
            model_name='privateimageupload',
            name='district',
            field=models.ForeignKey(blank=True, help_text='The district whom this image belongs to.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='private_image_uploads', to='tenant_foundation.District'),
        ),
        migrations.AddField(
            model_name='privateimageupload',
            name='watch',
            field=models.ForeignKey(blank=True, help_text='The watch whom this image belongs to.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='private_image_uploads', to='tenant_foundation.Watch'),
        ),
    ]
