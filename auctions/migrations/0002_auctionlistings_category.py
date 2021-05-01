# Generated by Django 3.1.6 on 2021-04-15 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='AuctionListings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('discription', models.TextField(blank=True)),
                ('starting_bid', models.FloatField()),
                ('current_price', models.FloatField(default=models.FloatField())),
                ('photo', models.CharField(blank=True, max_length=2083)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('listed_by', models.CharField(blank=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ManyToManyField(to='auctions.Category')),
            ],
            options={
                'verbose_name': 'AuctionListing',
                'verbose_name_plural': 'AuctionListings',
                'ordering': ['-created_at'],
            },
        ),
    ]
