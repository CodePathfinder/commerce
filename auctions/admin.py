from django.contrib import admin
from .models import User, Category, AuctionListings, Bid, Comments, Watchlist


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_superuser')
    list_display_links = ('id', 'username')
    search_fields = ('username',)


class AuctionListingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'starting_bid',
                    'current_price', 'created_at', 'is_active')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'discription')


class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'commodity', 'bidder', 'new_bid', 'created_at')
    list_display_links = ('id', 'commodity')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'commodity', 'content', 'author', 'created_at')
    list_display_links = ('id', 'commodity', 'author')
    search_fields = ('commodity', 'author')


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'commodity', 'on_watchlist')
    list_display_links = ('id', 'user')
    # search_fields = ('user',)


admin.site.register(User, UsersAdmin)
admin.site.register(Category)
admin.site.register(AuctionListings, AuctionListingsAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
