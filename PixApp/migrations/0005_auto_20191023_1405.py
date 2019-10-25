# Generated by Django 2.2.6 on 2019-10-23 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PixApp', '0004_auto_20191023_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='favorited_by_users',
            field=models.ManyToManyField(blank=True, null=True, related_name='favorite_comments', to='PixApp.User'),
        ),
        migrations.AlterField(
            model_name='post',
            name='favorited_by_users',
            field=models.ManyToManyField(blank=True, null=True, related_name='favorite_posts', to='PixApp.User'),
        ),
    ]
