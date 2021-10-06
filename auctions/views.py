from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import User, AuctionListings, Category, Bid, Comments, Watchlist
from .forms import NewBid, NewComment, NewListing
from .utils import \
    pagination, \
    verify_and_update_current_price, \
    determine_winner_of_closed_listing, \
    set_on_watchlist_flag, \
    list_with_added_highest_bid_user_made_for_each_watchlist_items


def index(request):
    commodities = AuctionListings.objects.exclude(is_active=False)

    page, is_paginated, next_url, prev_url = pagination(request, commodities)

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, "auctions/index.html", context)


def category(request, pk):

    cat = get_object_or_404(Category, pk=pk)
    commodities = AuctionListings.objects.filter(
        category=cat).exclude(is_active=False)

    page, is_paginated, next_url, prev_url = pagination(request, commodities)

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
        'cat': cat
    }

    return render(request, "auctions/category.html", context)


@login_required
def closed(request, pk):

    # update attribute "is_active" in AuctionListings object switching it to false
    closed_commodity = get_object_or_404(AuctionListings, id=pk)
    if request.method == "POST":
        closed_commodity.is_active = False
        closed_datetime_formatted = closed_commodity.updated_at.strftime(
            '%B %d, %Y')
        closed_commodity.save()

        winner = determine_winner_of_closed_listing(closed_commodity)

        if winner:
            messages.success(
                request, f"Auction for {closed_commodity.title} is closed by the seller on {closed_datetime_formatted}. The winner of the auction is {winner} with a winning bid ${closed_commodity.current_price:.2f}")
            # TODO: uncomment or delete
            # message = f"Auction for {closed_commodity.title} is closed by the seller on {closed_datetime_formatted}. The winner of the auction is {winner} with a winning bid ${closed_commodity.current_price:.2f}"
            # message_success = True
        # generate message in case no bids have been offered
        else:
            messages.success(
                request, f"Auction for {closed_commodity.title} is closed by the seller on {closed_datetime_formatted}. No bid has been offered")
            # message = f"Auction for {closed_commodity.title} is closed by the seller on {closed_datetime_formatted}. No bid has been offered"
            # message_success = True
            winner = ''
    else:
        messages.error(
            request, f"Something went wrong: auction for {closed_commodity.title} was not closed")
        # message = f"Something went wrong: auction for {closed_commodity.title} was not closed"
        # message_success = False
        winner = ''
    return render(request, 'auctions/closed.html', {
        'commodity': closed_commodity,
        # 'message': message,
        # 'message_success': message_success,
        'winner': winner
    })


def bid(request, pk):

    commodity = get_object_or_404(AuctionListings, id=pk)
    comments = Comments.objects.filter(commodity=commodity)
    verify_and_update_current_price(commodity)

    if request.method == "POST":
        form = NewBid(request.POST)

        if form.is_valid():
            new_bid = form.cleaned_data['new_bid']

            # Get number of bids at moment of this post request
            n = Bid.objects.filter(commodity=commodity).count()

            # Verify is new_bid is greater than the current price (the highest bid) or at least as large as the starting bid (if no bids)
            if n and new_bid > commodity.current_price \
                    and new_bid > commodity.starting_bid \
                    or not n and new_bid >= commodity.starting_bid:
                bid = Bid(
                    commodity=commodity,
                    bidder=request.user,
                    new_bid=new_bid
                )
                # Save new bid object and update two fields (current_price and updated_at) AuctionListings table re commodity at issue
                bid.save()
                commodity.current_price = bid.new_bid
                commodity.save()
                message = "Your bid is placed"
                message_success = True
            else:
                if n:
                    messages.warning(
                        request, "New bid shall be greater than highest bid (current price)")
                else:
                    messages.warning(
                        request, "New bid shall be at least as large as the starting price")
        else:
            messages.error(request, "Validation error")
    else:
        pass

    bids_n = Bid.objects.filter(
        commodity=commodity, new_bid__gte=commodity.starting_bid).count()
    if request.user.is_authenticated:
        on_watchlist = set_on_watchlist_flag(request.user, commodity)
    else:
        on_watchlist = False
    winner = determine_winner_of_closed_listing(commodity)
    if not request.user.is_authenticated:
        messages.warning(
            request, "Please sign in to place a bid, set a watchlist, or leave a comment")
    elif winner == request.user.get_username and not commodity.is_active:
        messages.success(
            request, f"Congratulations! You are the winner of the listing: {commodity.title} for ${commodity.current_price}")

    context = {
        'commodity': commodity,
        'comments': comments,
        'form': NewBid(),
        'bids_n': bids_n,
        'comments_n': comments.count(),
        'on_watchlist': on_watchlist,
        'winner': winner
    }
    return render(request, "auctions/bid.html", context)


@ login_required
def create(request):

    if request.method == 'POST':
        form = NewListing(request.POST)
        if form.is_valid():
            categories = form.cleaned_data['category'].values_list(
                'title', flat=True)
            new_listing = AuctionListings.objects.create(
                title=form.cleaned_data['title'],
                discription=form.cleaned_data['discription'],
                starting_bid=form.cleaned_data['starting_bid'],
                current_price=form.cleaned_data['starting_bid'],
                photo=form.cleaned_data['photo'],
                listed_by=request.user,
            )
            cats = Category.objects.filter(title__in=categories)
            new_listing.category.set(cats)
            new_listing.save()
            return redirect('bid', new_listing.pk)
        else:
            form = NewListing(form)
            messages.error(request, "Validation error")
    else:
        form = NewListing()
    context = {
        'form': form
    }
    return render(request, "auctions/create.html", context)


@ login_required
def add_comment(request, pk):
    commodity = get_object_or_404(AuctionListings, id=pk)
    if request.method == 'POST':
        form = NewComment(request.POST)
        if form.is_valid():
            comment = Comments(
                commodity=commodity,
                content=form.cleaned_data['content'],
                author=request.user
            )
            comment.save()
            return redirect('bid', pk)
        else:
            form_comment = NewComment(form)
    else:
        form_comment = NewComment()
    context = {
        'commodity': commodity,
        'form_comment': form_comment
    }
    return render(request, "auctions/add_comment.html", context)


@ login_required
def watchlist(request):
    if request.method == 'POST':

        # ID for the respective commodity is taken from bid.html or watchlist.html form through POST
        id = int(request.POST['commodity_id'])

        commodity = get_object_or_404(AuctionListings, id=id)

        # Check if the commodity at issue was earlier registered on user's watchlist
        wl = Watchlist.objects.filter(
            user=request.user, commodity=commodity)

        # Option 1: earlier registered commodity is found. Switch the flag "on_watchlist". If flag is switched to True, the commodity is "added" (in fact, shown/restored/activated) on the watchlist. If flag is switched to False, the commodity is "removed" (in fact, hidden/disactivated) from the watchlist.
        if wl.count():
            wl = wl.get()
            if wl.on_watchlist == True:
                wl.on_watchlist = False
                messages.success(
                    request, f"{wl.commodity.title} is removed from the watchlist")
            else:
                wl.on_watchlist = True
                messages.success(
                    request, f"{wl.commodity.title} is added to the watchlist")
            wl.save()

        # Option 2: commodity has never been registered on user's watchlist. If flag is switched to True, the commodity is added as newly created Watchlist object.
        else:
            wl_item = Watchlist(
                user=request.user,
                commodity=commodity,
                on_watchlist=True
            )
            wl_item.save()
            messages.success(
                request, f"{wl_item.commodity.title} is added to the watchlist")
    else:
        pass

    commodities_on_watchlist = list_with_added_highest_bid_user_made_for_each_watchlist_items(
        request.user)

    page, is_paginated, next_url, prev_url = pagination(
        request, commodities_on_watchlist)

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
        'count': commodities_on_watchlist.count(),
    }

    return render(request, 'auctions/watchlist.html', context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password.")
            return redirect("login")
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return redirect("register")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username is already taken.")
            return redirect("register")

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
