# Generated by Django 4.0.2 on 2022-02-06 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_company_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='file',
            field=models.FileField(upload_to='fileCSV'),
        ),
    ]
