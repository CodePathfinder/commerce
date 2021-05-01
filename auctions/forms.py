from .models import AuctionListings, Bid, Comments
from django import forms


class NewBid(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ['new_bid', ]
        widgets = {
            'new_bid': forms.NumberInput(attrs={'class': 'form-control'})
        }
        labels = {'new_bid': ''}


class NewComment(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['content', ]
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Add your comment here ...'})
        }
        labels = {'content': ''}


class NewListing(forms.ModelForm):

    class Meta:
        model = AuctionListings
        fields = ['title', 'discription', 'starting_bid', 'photo', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'discription': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
