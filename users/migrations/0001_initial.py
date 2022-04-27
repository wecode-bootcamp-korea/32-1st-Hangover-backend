# Generated by Django 4.0.4 on 2022-04-26 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('count', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'friends',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('cart', models.ManyToManyField(null=True, through='users.Cart', to='products.product')),
                ('friend', models.ManyToManyField(null=True, through='users.Friend', to='users.user')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.AddField(
            model_name='friend',
            name='friend_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_from', to='users.user'),
        ),
        migrations.AddField(
            model_name='friend',
            name='friend_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_to', to='users.user'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prebuyer', to='users.user'),
        ),
    ]
