# Generated by Django 3.1.6 on 2021-04-17 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_bid_comments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ['-new_bid'], 'verbose_name': 'Bid', 'verbose_name_plural': 'Bids'},
        ),
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Comments'},
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='comment_text',
            new_name='content',
        ),
    ]