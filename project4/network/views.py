from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Posts
import json
from django.views.decorators.csrf import csrf_exempt

from .models import *


def index(request):
    all_posts = Posts.objects.all().order_by("id").reverse()

    objects = all_posts
    paginator = Paginator(objects, 10)

    page_number = request.GET.get('page')

    try:
        # Get the posts for the current page
        page_posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        page_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results
        page_posts = paginator.page(paginator.num_pages)

    likes = []
    try:
        list_of_likes = Likes.objects.filter(user=request.user)
        for positive_relation in list_of_likes:
            likes.append(positive_relation.post.id)
    except:
        likes = []




    return render(request, "network/index.html" ,{
        'page_posts': page_posts, 'likes':likes
    })



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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post(request):
    current_user = request.user
    post = request.POST["new_post"]
    new_comment = Posts(author = current_user, comment_content = post)
    new_comment.save()
    return HttpResponseRedirect(reverse("index"))

def profile(request, user):
    try:
        user_details = User.objects.get(username=user)
    except:
        user_details = None
        return render(request, "network/error.html", {
        "error_message":"User doesn't exist"})

    try:
        user_relationship = Follow.objects.get(user=request.user,other_user=user_details)
        user_following = True
    except:
        user_following = False
    
    if user_details == request.user:
        self_user = True
    else:
        self_user = False

    following = Follow.objects.filter(user=user_details)
    number_following = len(following)

    followers = Follow.objects.filter(other_user=user_details)
    number_followers = len(followers)
    

    user_posts = Posts.objects.filter(author=user_details).order_by("id").reverse()

    objects = user_posts
    paginator = Paginator(objects, 10)

    page_number = request.GET.get('page')

    try:
        # Get the posts for the current page
        page_posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        page_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results
        page_posts = paginator.page(paginator.num_pages)

    likes = []
    try:
        list_of_likes = Likes.objects.filter(user=request.user)
        for positive_relation in list_of_likes:
            likes.append(positive_relation.post.id)
    except:
        likes = []

    return render(request, "network/profile.html", {
        "page_posts":page_posts, "user_following":user_following, "user_name":user, "self_user":self_user, "number_following":number_following, "number_followers":number_followers, 'likes':likes
    })

def Add_Follow(request, user):
    current_user = request.user
    second_user = User.objects.get(username=user)
    new_relation = Follow(user=current_user,other_user=second_user)
    new_relation.save()
    return HttpResponseRedirect(reverse("profile",args=[user]))

def remove_follow(request, user):
    current_user = request.user
    second_user = User.objects.get(username=user)
    try:
        user_relationship = Follow.objects.get(user=current_user,other_user=second_user)
        user_relationship.delete()
    except:
        return render(request, "network/error.html", {
        "error_message":"User not following"})
        # create error
    return HttpResponseRedirect(reverse("profile",args=[user]))



def following(request):
    user_self = request.user
    users_followed = Follow.objects.filter(user=user_self)
    all_posts = Posts.objects.all().order_by("-id")

    relevant_post = []

    for post in all_posts:
        for relation in users_followed:
            if post.author == relation.other_user:
                relevant_post.append(post)
    
    objects = relevant_post
    paginator = Paginator(objects, 10)

    page_number = request.GET.get('page')

    try:
        # Get the posts for the current page
        page_posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        page_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results
        page_posts = paginator.page(paginator.num_pages)

    likes = []
    try:
        list_of_likes = Likes.objects.filter(user=request.user)
        for positive_relation in list_of_likes:
            likes.append(positive_relation.post.id)
    except:
        likes = []





    return render(request, "network/following.html", {
        'page_posts': page_posts, 'likes':likes
    })

@csrf_exempt
def Edit(request, id):
    data = json.loads(request.body)
    new_content = data.get("new_content")
    updated_post = Posts.objects.get(id=id)
    updated_post.comment_content = new_content
    updated_post.save()
    return JsonResponse({"message":"success"})

@csrf_exempt
def add_like(request):
    data = json.loads(request.body)
    post_id = data.get("id")
    post_data = Posts.objects.get(id=post_id)
    new_like = Likes(user=request.user, post=post_data)
    new_like.save()
    return JsonResponse({"message":"success"})

@csrf_exempt
def remove_like(request):
    data = json.loads(request.body)
    post_id = data.get("id")
    post_data = Posts.objects.get(id=post_id)
    remove_like = Likes.objects.get(user=request.user, post=post_data)
    remove_like.delete()
    return JsonResponse({"message":"success"})

def like_counter(request, id):
    post_data = Posts.objects.get(id=id)
    all_post_likes = Likes.objects.filter(post=post_data)
    current_likes = len(all_post_likes)
    return JsonResponse({"current_likes":current_likes})

def all_posts(request):
    posts = Posts.objects.all()
    number_of_posts = len(posts)
    return JsonResponse({"number_of_posts":number_of_posts})