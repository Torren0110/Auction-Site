from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Item(models.Model):
    user = models.ForeignKey(User, related_name='Item_from', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default = timezone.now)
    initial_bid = models.PositiveIntegerField()
    current_bid = models.PositiveIntegerField(null=True)
    current_bidder = models.ForeignKey(User, related_name='current_bidder', on_delete=models.DO_NOTHING, null=True, default=None)
    paid = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    address = models.CharField(max_length=200, null=True, default=None)


    def __str__(self):
        return self.name

class ItemPhoto(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='item_images', blank=True)

    def __str__(self):
        return f'{self.item} Image'