from django.shortcuts import render, redirect, HttpResponse
from .models import Item, ItemPhoto
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .forms import ItemEnlistForm, ImageFormSet
from django.http import Http404, JsonResponse

DEFAULT_IMG_URL = settings.MEDIA_URL + "/item_images/default.webp"

# Create your views here.

def home(request):
    live_items = Item.objects.filter(start_time__lte = timezone.now(), end_time__gt = timezone.now())
    live_items = [[item, ItemPhoto.objects.filter(item = item).first()] for item in live_items]
    
    unlive_items = Item.objects.filter(start_time__gt = timezone.now())
    unlive_items = [[item, ItemPhoto.objects.filter(item = item).first()] for item in unlive_items]

    if(request.user.is_authenticated):
        items_won = [item for item in Item.objects.filter(current_bidder = request.user, end_time__lt = timezone.now(), paid = False)]
        items_sold = [item for item in Item.objects.filter(user = request.user, paid = True, shipped=False)]
    else:
        items_won = []
        items_sold = []

    context = {
        'live_items' : live_items,
        'unlive_itmes' : unlive_items,
        'now' : timezone.now(),
        'default_img_url' : DEFAULT_IMG_URL,
        'items_won' : items_won,
        'items_sold' : items_sold
    }

    return render(request, 'auction/home.html', context = context)

def view_item(request, pk):
    item = Item.objects.get(pk = pk)
    images = ItemPhoto.objects.filter(item=item)

    if not images.exists():
        images = [{'photo' : {'url' : DEFAULT_IMG_URL}}]

    context = {
        'item' : item,
        'images' : images
    }

    return render(request, 'auction/view_item.html', context=context)

@login_required
def bid(request, pk):
    item = Item.objects.get(pk=pk)

    if(item.start_time > timezone.now()):
        messages.warning(request, "This item is not live yet")
        return redirect('item', pk = item.id)

    if request.method == "POST":
        user = request.user
        bid_ammount = request.POST.get('bid_ammount')
        bid_ammount = int(bid_ammount)

        if((item.current_bid == None and bid_ammount >= item.initial_bid) or (item.current_bid and bid_ammount > item.current_bid)):
            item.current_bid = bid_ammount
            item.current_bidder = user
            item.save()
            messages.success(request, 'You are currently the highest bidder.')
        else:
            messages.warning(request, 'you can not bid less than or equal to the current bid.')


    context = {
        'item' : item,
    }

    return render(request, 'auction/bid.html', context=context)

@login_required
def sell(request):
    if request.method == 'POST':
        item_form = ItemEnlistForm(request.POST, request.FILES)
        image_formset = ImageFormSet(request.POST, request.FILES, instance=Item())
        
        if item_form.is_valid() and image_formset.is_valid():
            item = item_form.save(user = request.user)
            image_formset.instance = item
            image_formset.save()
            return redirect('item', pk = item.pk)

    else:
        item_form = ItemEnlistForm()
        image_formset = ImageFormSet(instance=Item())


    context = {
        'item_form': item_form,
        'image_formset': image_formset
    }

    return render(request, 'auction/sell.html', context=context)

@login_required
def myBids(request):
    items = Item.objects.filter(current_bidder = request.user)
    items = [[item, ItemPhoto.objects.filter(item = item).first()] for item in items]
    context = {
        'items' : items,
        'now' : timezone.now(),
        'default_img_url' : DEFAULT_IMG_URL
    }

    return render(request, 'auction/myBids.html', context=context)

@login_required
def myListing(request):
    items = Item.objects.filter(user = request.user)
    items = [[item, ItemPhoto.objects.filter(item = item).first()] for item in items]

    context = {
        'items' : items,
        'now' : timezone.now(),
        'default_img_url' : DEFAULT_IMG_URL
    }

    return render(request, 'auction/myListing.html', context=context)

@login_required
def pay(request, pk):
    item = Item.objects.get(id=pk)
    if item.current_bidder == request.user:
        if item.paid:
            messages.success(request, 'You have already paid for the item.')
            return redirect('home')
        if request.method == 'POST':
            item.address = request.POST.get('addr')
            item.paid = True
            item.save()
            
            messages.success(request, 'Payment Successfull')
            return redirect(home)
        else:
            return render(request, 'auction/pay.html', context={'item' : item})
    else:
        raise Http404('Page Not found')
    
@login_required
def ship(request, pk):
    item = Item.objects.get(id=pk)
    if item.user == request.user:
        if item.shipped:
            messages.success(request, 'You have already shipped this item.')
        elif item.paid:
            if(request.method == 'POST'):
                item.shipped = True
                item.save()
                messages.success(request, 'You have successfully shiped the item.')
            else:
                return render(request, 'auction/ship.html', context={'item' : item})
        else:
            messages.success(request, "The highest has not made the payment yet.")
        return redirect('home')
    else:
        raise Http404('Page not found')
    
def getSearch(request):
    if request.method == 'GET':
        searchText = request.GET.get('text')
        if searchText:
            searchResults = Item.objects.filter(name__contains=searchText).values('name')
            searchResults = [item['name'] for item in searchResults]
        else:
            return HttpResponse()

        if(len(searchResults) == 0):
            return HttpResponse()

        searchResults = JsonResponse(searchResults, safe=False)
        return searchResults

    return HttpResponse()

def search(request):
    if(request.method == "GET"):
        searchString = request.GET['search_string']

        live_items = Item.objects.filter(name__contains = searchString, start_time__lte = timezone.now(), end_time__gt = timezone.now())
        live_items = [[item, ItemPhoto.objects.filter(item = item).first()] for item in live_items]
    
        unlive_items = Item.objects.filter(name__contains = searchString, start_time__gt = timezone.now())
        unlive_items = [[item, ItemPhoto.objects.filter(item = item).first()] for item in unlive_items]

        if(not len(live_items) and not len(unlive_items)):
            messages.warning(request, "No Items Match.")

        context = {
            'live_items' : live_items,
            'unlive_itmes' : unlive_items,
            'now' : timezone.now(),
            'default_img_url' : DEFAULT_IMG_URL,
            'searchString' : searchString,
        }

        return render(request, 'auction/home.html', context = context)

    messages.warning(request, "No Items Match.")
    return redirect('home')