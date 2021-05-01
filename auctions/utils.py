from .models import Bid, Watchlist
from django.db.models import Max


def verify_and_update_current_price(commodity):
    """ Check if the highest bid for certain listing item in the Bid model corresponds to current price attribute for the same item in AuctionListings model. If not current price attribute is updated """

    highest_bid = Bid.objects.filter(
        commodity=commodity).aggregate(Max('new_bid')).get('new_bid__max')
    if highest_bid == None:
        commodity.current_price = commodity.starting_bid
    else:
        if highest_bid > commodity.starting_bid and highest_bid > commodity.current_price:
            commodity.current_price = highest_bid
    commodity.save()


def determine_winner_of_closed_listing(commodity):
    """ Detemine the name of the winner for the closed listing based on Bid model records"""

    if not commodity.is_active:
        if Bid.objects.filter(commodity=commodity.id).count():
            winner = Bid.objects.get(commodity=commodity.id,
                                     new_bid=commodity.current_price).bidder.get_username()
        else:
            winner = ''
    else:
        winner = ''
    return winner


def set_on_watchlist_flag(user, commodity):
    """ Check if commodity is or have ever been on watchlist and either extract on_watchlist status from watchlist records or set it to False"""

    commodity_watchlist_status = Watchlist.objects.filter(
        user=user, commodity=commodity)

    if commodity_watchlist_status.count():
        on_watchlist = commodity_watchlist_status.values_list(
            'on_watchlist', flat=True).get()
    else:
        on_watchlist = False
    return on_watchlist


def add_highest_bid_user_made_for_each_watchlist_items(user):

    # get list of commodities as dict objects added by active user to his/her watchlist
    commodities_shortlist = Watchlist.objects.filter(
        user=user).exclude(on_watchlist=False).values('commodity__pk', 'commodity__title', 'commodity__photo', 'commodity__starting_bid', 'commodity__current_price', 'commodity__discription', 'commodity__is_active', 'commodity__listed_by__username')

    # iterate commodities_shortlist queryset and add extra attribute 'user_highest_bid' for each commodity (python dictionary) in commodities_shortlist

    for item in commodities_shortlist:
        user_highest_bid = Bid.objects.filter(
            commodity=item['commodity__pk']).filter(
            bidder=user).order_by('-new_bid').values('new_bid', 'created_at').first()
        if user_highest_bid == None:
            item['user_highest_bid'] = 0
        else:
            item['user_highest_bid'] = user_highest_bid['new_bid']
            item['user_highest_bid_created_at'] = user_highest_bid['created_at']

    return commodities_shortlist
