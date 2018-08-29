# Generated by Django 2.1 on 2018-08-26 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_project', '0006_auto_20180825_0221'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['pinned', '-created_at']},
        ),
        migrations.AlterModelOptions(
            name='roles',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='roles',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='roles',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]