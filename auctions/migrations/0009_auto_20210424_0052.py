# Generated by Django 3.1.6 on 2021-04-24 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210420_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='discription',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]