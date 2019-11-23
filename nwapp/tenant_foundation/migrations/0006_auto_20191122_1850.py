# Generated by Django 2.2.7 on 2019-11-22 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0005_auto_20191122_0357'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membermetric',
            old_name='how_hear_other',
            new_name='how_did_you_hear_other',
        ),
        migrations.RemoveField(
            model_name='membermetric',
            name='how_hear',
        ),
        migrations.AddField(
            model_name='membermetric',
            name='how_did_you_hear',
            field=models.ForeignKey(blank=True, help_text='How the member heard about the NWApp.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_metric_how_did_you_hear_items', to='tenant_foundation.HowHearAboutUsItem'),
        ),
        migrations.AlterModelTable(
            name='howhearaboutusitem',
            table='nwapp_how_did_you_hear_about_us_items',
        ),
    ]