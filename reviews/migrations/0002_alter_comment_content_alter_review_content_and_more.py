# Generated by Django 4.0.4 on 2022-04-27 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterModelTable(
            name='reviewlike',
            table='review_likes',
        ),
    ]
