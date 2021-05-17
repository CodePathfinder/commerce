''' Replaced in full with context_processor.py'''

# from django import template
# from django.db.models import Count
# from auctions.models import Category, Watchlist, User


# register = template.Library()


# @register.simple_tag(name='get_list_categories')
# def get_categories():
#     return Category.objects.all()


# @register.simple_tag(name='count_watchlist_items')
# def count_items():
#     return User.objects.filter(watchlist__on_watchlist=True).annotate(num = Count('watchlist'))