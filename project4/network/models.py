from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    comment_content =  models.CharField(max_length=400)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} {self.comment_content}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    other_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follower")

    def __str__(self):
        return f"{self.user} follows {self.other_user}"
    
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="post_like")
    
    def __str__(self):
        return f"{self.user} likes {self.post}"