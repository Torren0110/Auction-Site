from django.urls import path
from .views import home, view_item, bid, sell, pay, myBids, myListing, getSearch, ship, search

urlpatterns = [
    path('', home, name = 'home'),
    path('item/<int:pk>/', view_item, name = 'item'),
    path('item/bid/<int:pk>/', bid, name = 'bid'),
    path('sell/', sell, name='sell'),
    path('pay/<int:pk>/', pay, name='pay'),
    path('ship/<int:pk>/', ship, name='ship'),
    path('myBids/', myBids, name='myBids'),
    path('myListing/', myListing, name='myListing'),
    path('getSearch/', getSearch, name='getSearch'),
    path('search/', search, name='search')
]