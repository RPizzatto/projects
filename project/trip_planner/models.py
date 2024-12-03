from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Create your models here.

class Category(models.Model):
    type = models.CharField(max_length=400)
   
    def __str__(self):
        return f"{self.type}"
    
class Trip(models.Model):
    title = models.CharField(max_length=400)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="traveller")
    image = models.ImageField(upload_to='images/', default='images/default.jpg')
   
    def __str__(self):
        return f"{self.title}"

class Activity(models.Model):
    title = models.CharField(max_length=400)
    activity_date_time = models.DateTimeField(blank=True,null=True)
    city = models.CharField(max_length=400, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_activity")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_activity")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_category")
    image = models.ImageField(upload_to='images/activity')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.CharField(max_length=1000)
    
    def __str__(self):
        return f"{self.title}"
    
class Hotel(models.Model):

    name = models.CharField(max_length=400)
    city = models.CharField(max_length=400, blank=True, null=True)
    entry_date = models.DateField()
    exit_date = models.DateField()
    number_of_nights = models.IntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_hotel")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_hotel")
    image = models.ImageField(upload_to='images/hotel')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    contact = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True,null=True, related_name="category_hotel")
    
    def __str__(self):
        return f"{self.name}"

class Flight(models.Model):

    airline = models.CharField(max_length=400)
    departure_date_time = models.DateTimeField()
    arrival_date_time = models.DateTimeField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_flight")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_flight")
    departure_airport = models.CharField(max_length=400)
    arrival_airport = models.CharField(max_length=400)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    flight_number = models.CharField(max_length=10)
    reservation_code = models.CharField(max_length=6)
    notes = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True,null=True, related_name="category_flight")
    
    def __str__(self):
        return f"flight to {self.arrival_airport}"
    
class Restaurant(models.Model):

    restaurant_name = models.CharField(max_length=400)
    restaurant_date_time = models.DateTimeField()
    city = models.CharField(max_length=400, blank=True, null=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_restaurant")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_restaurant")
    price = models.DecimalField(decimal_places=2, max_digits=10)
    notes = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null=True, related_name="category_restaurant")
    image = models.ImageField(upload_to='images/restaurant' ,blank=True,null=True)

    def __str__(self):
        return f"{self.restaurant_name}"
    
