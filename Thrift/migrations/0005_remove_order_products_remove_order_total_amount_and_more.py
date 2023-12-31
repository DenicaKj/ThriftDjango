# Generated by Django 4.2.2 on 2023-06-29 02:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Thrift', '0004_product_date_accepted_product_date_sent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_amount',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Thrift.product'),
            preserve_default=False,
        ),
    ]
