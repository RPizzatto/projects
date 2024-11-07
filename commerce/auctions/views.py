from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *


def index(request):
    #title, description, current price, and photo
    active_listing = Listing.objects.filter(status = True)
    
    return render(request, "auctions/index.html", {
        "active_listing":active_listing
    })

def closed_listing(request):
    #title, description, current price, and photo
    active_listing = Listing.objects.filter(status = False)
    
    return render(request, "auctions/index.html", {
        "active_listing":active_listing
    })


#If method POST function authenticate user's input. If valid, log user in and redirect to index page. Error message if invalid information.
#If method GET display the login page
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html")
    else:
        #collect data from HTML form 
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.POST["image"]
        category = request.POST["category"]
        current_user = request.user
        #insert new row in listing database
        new_row = Listing(title=title, description=description, starting_bid=starting_bid,image=image,category=category,user=current_user)
        new_row.save()
        #insert new row in acquisition database
        minimal_bid = Acquisition(user=current_user,item=new_row,value=starting_bid)
        minimal_bid.save()
        url = reverse('index')
        return redirect(url)

def listing(request, listing_id):
    try:
        listing_data = Listing.objects.get(id=listing_id) 

    except Listing.DoesNotExist:
        return render(request, "auctions/error.html" ,{
                "message":"Listing does not exist"
            })
    
    try:
        watchlist_data = Watch_list.objects.get(user=request.user,item=listing_data)
        match = True
    except:
        match = False

    bid_list = Acquisition.objects.filter(item=listing_data)
    last_bid_data = bid_list.last()
    last_bid_value = last_bid_data.value
    #find the user who post the last bid
    

    all_comments = Comment.objects.filter(item=listing_data)

    listing_status = listing_data.status
    listing_owner = listing_data.user
    if listing_status == True and listing_owner == request.user:
        selling_button = True
    else:
        selling_button = False

    last_bid_user = last_bid_data.user
    if listing_status == False and last_bid_user == request.user:
        winning_message = True
    else:
        winning_message = False


     

    return render(request, "auctions/listing.html", {
        "listing_data":listing_data, "last_bid_value": last_bid_value, "match":match, "all_comments":all_comments, "selling_button":selling_button, "winning_message":winning_message
    })
        

def display_category(request):
    if request.method == "POST":
        selected_category = request.POST["category"]

        category_filter = Listing.objects.filter(category=selected_category, status = True)
        return render(request, "auctions/index.html", {
            "active_listing":category_filter
        })

def new_bid(request, listing_id):
    if request.method == "POST":
        novo_bid = request.POST["bid"]
        message = "you are stupid"
        try:
            listing_data = Listing.objects.get(id=listing_id)  
        except Listing.DoesNotExist:
            return render(request, "auctions/error.html", {
                "message":message
            })
        bid_list = Acquisition.objects.filter(item=listing_data)
        last_bid_data = bid_list.last()
        last_bid_value = last_bid_data.value
        if float(novo_bid) <= last_bid_value: 
            return render(request, "auctions/error.html", {
                "message":"Your bid is too low"
            })
        else:
            updated_bid = Acquisition(
                user=request.user, 
                item=listing_data,
                value=float(novo_bid)
            )
            updated_bid.save()
            url = reverse('listing', args=[listing_id])
            return redirect(url)
    
    
def comment(request, listing_id):
    if request.method == "POST":
        latest_comment = request.POST["comment"]
        listing_details = Listing.objects.get(id=listing_id)
        new_comment = Comment(
            user=request.user,
            item=listing_details,
            comments=latest_comment
        )
        new_comment.save()
        url = reverse('listing', args=[listing_id])
        return redirect(url)

def add_watchlist(request, listing_id):
    listing_details = Listing.objects.get(id=listing_id)
    new_item = Watch_list(
        user=request.user,
        item=listing_details
    )
    new_item.save()
    url = reverse('listing', args=[listing_id])
    return redirect(url) 

def remove_watchlist(request, listing_id):
    listing_details = Listing.objects.get(id=listing_id)
    remove_item = Watch_list.objects.get(user=request.user, item=listing_details)
    remove_item.delete()
    url = reverse('listing', args=[listing_id])
    return redirect(url) 

def watchlist(request):
    current_user = request.user
    user_watchlist = Watch_list.objects.filter(user=current_user)
    return render(request, "auctions/watchlist.html", {
        "user_watchlist":user_watchlist
    })

def close_auction(request, listing_id):
    mudar_status = Listing.objects.get(id=listing_id)
    mudar_status.status = False
    mudar_status.save()
    url = reverse('listing', args=[listing_id])
    return redirect(url)



   




        
