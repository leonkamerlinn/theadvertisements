# Generated by Django 2.1 on 2018-08-07 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
