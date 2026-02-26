from django.db import models
from django.conf import settings 

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Destination(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='static/images/')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=5000)
    seats_filled = models.IntegerField(default=0) 

    def seats_left(self):
        left = 3 - self.seats_filled
        return left if left > 0 else 0

    def is_full(self):
        return self.seats_filled >= 3

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=100)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.destination.name}"