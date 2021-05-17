from django.db.models import Count
from .models import Category, User

def get_categories(request):
	categories = Category.objects.all()
	return dict(categories=categories)


def count_watchlist_items(request):
    return User.objects.filter(watchlist__on_watchlist=True).filter(username=request.user).aggregate(num_watched = Count('watchlist'))