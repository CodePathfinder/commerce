from django import template

from auctions.models import Category, Watchlist, User

register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()
