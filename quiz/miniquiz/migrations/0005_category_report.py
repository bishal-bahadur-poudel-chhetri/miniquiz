# Generated by Django 4.0.3 on 2022-05-21 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniquiz', '0004_follower_alter_category_categoryimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='report',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
