from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=400)
    starting_bid = models.FloatField() 
    image = models.CharField(max_length=400)
    category = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} {self.title}"

class Acquisition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_history")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_history")
    value = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.item} {self.date}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_details")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_details")
    comments = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.item} {self.comments} {self.date}"
    
class Watch_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watch")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_watch")

    def __str__(self):
        return f"{self.item} {self.user}"