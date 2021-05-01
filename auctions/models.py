from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse


class User(AbstractUser):

    def __str__(self):
        return self.username


class Category(models.Model):

    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']


class AuctionListings(models.Model):

    title = models.CharField(max_length=100)
    discription = models.TextField()
    starting_bid = models.FloatField()
    current_price = models.FloatField(blank=True)
    photo = models.CharField(max_length=2083, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    category = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bid', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'AuctionListing'
        verbose_name_plural = 'AuctionListings'
        ordering = ['-created_at']


class Bid(models.Model):

    commodity = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    new_bid = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.new_bid)

    class Meta:
        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'
        ordering = ['-new_bid']


class Comments(models.Model):
    commodity = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"New comment for {self.commodity} is {self.content}"

    class Meta:
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commodity = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    on_watchlist = models.BooleanField(default=False)

    def __str__(self):
        return self.commodity.title
