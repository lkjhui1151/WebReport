# Generated by Django 4.0.2 on 2022-02-07 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_company_csv_alter_company_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='file',
        ),
        migrations.AddField(
            model_name='company',
            name='csv',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.company_csv'),
        ),
    ]
