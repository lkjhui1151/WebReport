# Generated by Django 4.0.2 on 2022-02-07 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_company_csv_company_company_csv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='csv',
        ),
        migrations.AlterField(
            model_name='company',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
