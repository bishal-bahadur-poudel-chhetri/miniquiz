# Generated by Django 4.0.3 on 2022-08-25 05:50

from django.db import migrations, models
import django.db.models.deletion
import miniquiz.models


class Migration(migrations.Migration):

    dependencies = [
        ('miniquiz', '0004_alter_leaderboards_authorsid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miniquiz.questions'),
        ),
        migrations.AlterField(
            model_name='category',
            name='categoryImage',
            field=models.ImageField(blank=True, default=miniquiz.models.get_default_profile_image, null=True, upload_to=miniquiz.models.get_profile_image_filepath),
        ),
        migrations.AlterField(
            model_name='leaderboards',
            name='categoryIdentity',
            field=models.ForeignKey(default='b99e7969-11d1-4297-a14f-fdf42c8aaa3', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='category_id', to='miniquiz.category'),
        ),
    ]
