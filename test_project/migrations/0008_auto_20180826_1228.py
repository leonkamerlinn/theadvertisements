# Generated by Django 2.1 on 2018-08-26 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_project', '0007_auto_20180826_0827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replay',
            name='files',
        ),
        migrations.AddField(
            model_name='replay',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='./static'),
        ),
    ]
