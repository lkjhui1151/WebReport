# Generated by Django 4.0.2 on 2022-02-07 04:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_company_csv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company_csv',
            name='company',
        ),
        migrations.AddField(
            model_name='company',
            name='csv',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.company_csv'),
        ),
    ]
