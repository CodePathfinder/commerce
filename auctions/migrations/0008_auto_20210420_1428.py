# Generated by Django 3.1.6 on 2021-04-20 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='current_price',
            field=models.FloatField(blank=True),
        ),
    ]
