# Generated by Django 4.0.3 on 2022-06-21 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('miniquiz', '0003_alter_leaderboards_authorsid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaderboards',
            name='authorsID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorIdentity', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='leaderboards',
            name='categoryIdentity',
            field=models.ForeignKey(default='4f0b25fa-b880-4cdb-8adb-1a8511147060', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='category_id', to='miniquiz.category'),
        ),
    ]
