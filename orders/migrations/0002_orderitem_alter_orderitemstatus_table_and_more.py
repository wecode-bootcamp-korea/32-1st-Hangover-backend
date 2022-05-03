# Generated by Django 4.0.4 on 2022-04-27 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_alcohol_percentage_and_more'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
            options={
                'db_table': 'order_items',
            },
        ),
        migrations.AlterModelTable(
            name='orderitemstatus',
            table='order_item_statuses',
        ),
        migrations.AlterModelTable(
            name='ordershipment',
            table='order_shipments',
        ),
        migrations.AlterModelTable(
            name='orderstatus',
            table='order_statuses',
        ),
        migrations.DeleteModel(
            name='OrderItems',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order_item_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orderitemstatus'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='shipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.ordershipment'),
        ),
    ]
