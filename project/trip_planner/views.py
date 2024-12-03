from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime

from .models import *

# Create your views here.

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
            return render(request, "trip_planner/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "trip_planner/login.html")


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
            return render(request, "trip_planner/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "trip_planner/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "trip_planner/register.html")

def index(request):
    try:
        user = request.user
        current_user_trips = Trip.objects.filter(user=user)
       
        trips_with_budgets = []
        for trip in current_user_trips:
            trip_hotels = list(Hotel.objects.filter(trip=trip))
            trip_transportation = list(Flight.objects.filter(trip=trip))
            trip_restaurants = list(Restaurant.objects.filter(trip=trip))
            trip_activities = list(Activity.objects.filter(trip=trip))
            all_activities = trip_transportation + trip_hotels + trip_restaurants + trip_activities

            total_budget = 0
            for row in all_activities:
                if row.price:
                    total_budget += row.price

            # Add the budget directly to the trip dictionary
            trips_with_budgets.append({
                "trip": trip,
                "budget": round(total_budget),
            })

        return render(request, "trip_planner/index.html", {
            "trips_with_budgets": trips_with_budgets,
            "message": "You don't have an upcoming trip",
        })
    except Exception as e:
        print(f"Error: {e}")
        return HttpResponseRedirect(reverse("login"))




def new_trip(request):
    if request.method == "POST":
        trip_name = request.POST["trip_title"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        trip_image = request.FILES.get("image")
        current_user = request.user
        add_new_trip = Trip(title=trip_name, start_date=start_date, end_date=end_date, image=trip_image, user=current_user)
        add_new_trip.save()
        return HttpResponseRedirect(reverse("index"))


    else: 
        return render(request, "trip_planner/new_trip.html")
    
def trip(request, id):
    if request.method == "GET":
        current_trip = Trip.objects.get(id=id)
        
        current_user = request.user 
        if not current_trip.image or not current_trip.image.name:
            default_image = "../media/images/default.jpg"
        else:
            default_image = current_trip.image.url
        if current_user == current_trip.user:
            trip_hotels = list(Hotel.objects.filter(trip=current_trip))
            trip_transportation = list(Flight.objects.filter(trip=current_trip))
            trip_restaurants = list(Restaurant.objects.filter(trip=current_trip))
            trip_activities = list(Activity.objects.filter(trip=current_trip))
            all_activities = trip_transportation + trip_hotels + trip_restaurants + trip_activities

            def get_activity_date(activity):
                if isinstance(activity, Flight):
                    return activity.departure_date_time.date()  
                elif isinstance(activity, Hotel):
                    return activity.entry_date  
                elif isinstance(activity, Restaurant):
                    return activity.restaurant_date_time.date()  
                elif isinstance(activity, Activity):
                    return activity.activity_date_time.date() if activity.activity_date_time else datetime.max.date()  # Handle None
                else:
                    return datetime.max.date()
                
            all_activities_sorted = sorted(all_activities, key=get_activity_date)


            total_budget = 0
            for row in all_activities:
                if row.price:
                    total_budget += row.price
                      

            return render(request, "trip_planner/trip.html", {
                "current_trip": current_trip, "image":default_image, "all_activities":all_activities_sorted, "total_budget":round(total_budget)
            })
        else: 
            return render(request, "trip_planner/error.html", {
                "message": "You don't have access to this trip"
            })

def new_activity(request, id):
    if request.method == "GET":
        categories_list = Category.objects.all()

        return render(request, "trip_planner/new_activity.html", {
            "categories_list":categories_list, "id":id
        })
    else:
        category = request.POST["category"]
        category_row = Category.objects.get(type=category)
        user = request.user 
        current_trip = Trip.objects.get(id=id)
        if category == "Activity":
            activity_name = request.POST["activity_name"]
            activity_city = request.POST["activity_city"]
            activity_date = request.POST["activity_date"]
            activity_time = request.POST["activity_time"]
            activity_price = request.POST["activity_price"]
            if not activity_price:
                activity_price = 0
            else:
                activity_price = float(activity_price)
            activity_notes = request.POST["activity_notes"]
            activity_image = request.POST["activity_image"]
            if not activity_time:
                activity_time = "00:00"
            activity_date_time = datetime.strptime(f"{activity_date} {activity_time}", "%Y-%m-%d %H:%M")
            add_activity = Activity(title = activity_name, activity_date_time = activity_date_time, city = activity_city, category = category_row, trip=current_trip, user=user, price=activity_price, description=activity_notes, image = activity_image)
            add_activity.save()
            
        elif category == "Restaurant":
            restaurant_name = request.POST["restaurant_name"]
            restaurant_city = request.POST["restaurant_city"]
            restaurant_date = request.POST["restaurant_date"]
            restaurant_time = request.POST["restaurant_time"]
            restaurant_price = request.POST["restaurant_price"]
            if not restaurant_price:
                restaurant_price = 0
            else:
                restaurant_price = float(restaurant_price)
            restaurant_note = request.POST["restaurant_notes"]
            restaurant_image = request.POST["restaurant_image"]
            if not restaurant_time:
                restaurant_time = "00:00"
            restaurant_date_time = datetime.strptime(f"{restaurant_date} {restaurant_time}", "%Y-%m-%d %H:%M")
            add_restaurant = Restaurant(restaurant_name = restaurant_name, restaurant_date_time = restaurant_date_time, city = restaurant_city, category = category_row, trip=current_trip, user=user, price=restaurant_price, notes=restaurant_note, image = restaurant_image)
            add_restaurant.save()
            
        elif category == "Transportation":
            airline = request.POST["company"]
            reservation_code = request.POST["reservation_number"]
            flight_number = request.POST["flight_number"]
            departure_airport = request.POST["departure_city"]
            departure_date = request.POST["departure_date"]
            departure_time = request.POST["departure_time"]
            arrival_airport = request.POST["arrival_city"]
            arrival_date = request.POST["arrival_date"]
            arrival_time = request.POST["arrival_time"]
            price = request.POST["budget"]
            if not price:
                price = 0
            else:
                price = float(price)
            notes = request.POST["notes"]
            if not arrival_time:
                arrival_time = "00:00"
            arrival_date_time = datetime.strptime(f"{arrival_date} {arrival_time}", "%Y-%m-%d %H:%M")
            if not departure_time:
                departure_time = "00:00"
            departure_date_time = datetime.strptime(f"{departure_date} {departure_time}", "%Y-%m-%d %H:%M")
            add_transportation = Flight(airline=airline, departure_date_time = departure_date_time, category = category_row, trip=current_trip, user=user, arrival_airport=arrival_airport, departure_airport=departure_airport, price=price, flight_number=flight_number, notes=notes,  reservation_code=reservation_code, arrival_date_time=arrival_date_time)
            add_transportation.save()
            
        elif category == "Hotel":
            name = request.POST["hotel_name"]
            city = request.POST["hotel_city"]
            entry_date = request.POST["start_date"]
            exit_date = request.POST["end_date"]
            entry_date_obj = datetime.strptime(entry_date, "%Y-%m-%d").date()
            exit_date_obj = datetime.strptime(exit_date, "%Y-%m-%d").date()

            price = request.POST["budget"]
            if not price:
                price = 0
            else:
                price = float(price)
            contact = request.POST["hotel_contact"]
            image = request.POST["image"]
            number_of_nights = (exit_date_obj - entry_date_obj).days
            
            add_hotel = Hotel(name = name, entry_date = entry_date, exit_date = exit_date, city = city, category = category_row, trip=current_trip, user=user, price=price, contact =contact, image = image, number_of_nights=number_of_nights)
            add_hotel.save()
        return HttpResponseRedirect(reverse("trip",args=[id]))


def activity_details(request, category, id):
    if request.method == "GET":
        if category == "Activity":
            details = Activity.objects.get(id=id)
        elif category == "Hotel":
            details = Hotel.objects.get(id=id)
        elif category == "Transportation":
            details = Flight.objects.get(id=id)
        elif category == "Restaurant":
            details = Restaurant.objects.get(id=id)
        return render(request, "trip_planner/activity_details.html", {
            "details": details
            })
    
def edit_activity(request, category, id):
    if request.method == "GET":
        if category == "Activity":
            details = Activity.objects.get(id=id)
        elif category == "Hotel":
            details = Hotel.objects.get(id=id)
        elif category == "Transportation":
            details = Flight.objects.get(id=id)
        elif category == "Restaurant":
            details = Restaurant.objects.get(id=id)
        return render(request, "trip_planner/edit_activity.html", {
        "details":details
    } )

    else:
        if category == "Hotel":
            name = request.POST["hotel_name"]
            city = request.POST["hotel_city"]
            entry_date = request.POST["start_date"]
            exit_date = request.POST["end_date"]
            entry_date_obj = datetime.strptime(entry_date, "%Y-%m-%d").date()
            exit_date_obj = datetime.strptime(exit_date, "%Y-%m-%d").date()
            price = request.POST["budget"]
            if not price:
                price = 0
            else:
                price = float(price)
            contact = request.POST["hotel_contact"]
            image = request.POST["image"]
            number_of_nights = (exit_date_obj - entry_date_obj).days
            
            edit_hotel = Hotel.objects.get(id=id)
            edit_hotel.name = name
            edit_hotel.city = city
            edit_hotel.entry_date = entry_date_obj
            edit_hotel.exit_date = exit_date_obj
            edit_hotel.price = price
            edit_hotel.contact = contact
            edit_hotel.image = image
            edit_hotel.number_of_nights = number_of_nights
            edit_hotel.save()
        
        elif category == "Transportation":
            airline = request.POST["company"]
            reservation_code = request.POST["reservation_number"]
            flight_number = request.POST["flight_number"]
            departure_airport = request.POST["departure_city"]
            departure_date = request.POST["departure_date"]
            departure_time = request.POST["departure_time"]
            arrival_airport = request.POST["arrival_city"]
            arrival_date = request.POST["arrival_date"]
            arrival_time = request.POST["arrival_time"]
            price = request.POST["budget"]
            if not price:
                price = 0
            else:
                price = float(price)
            notes = request.POST["notes"]
            arrival_date_time = datetime.strptime(f"{arrival_date} {arrival_time}", "%Y-%m-%d %H:%M")
            departure_date_time = datetime.strptime(f"{departure_date} {departure_time}", "%Y-%m-%d %H:%M")

            edit_flight = Flight.objects.get(id=id)
            edit_flight.airline = airline
            edit_flight.departure_date_time = departure_date_time
            edit_flight.arrival_date_time = arrival_date_time
            edit_flight.departure_airport = departure_airport
            edit_flight.arrival_airport = arrival_airport
            edit_flight.price = price
            edit_flight.flight_number = flight_number
            edit_flight.reservation_code = reservation_code
            edit_flight.notes = notes
            edit_flight.save()

        elif category == "Activity":
            activity_name = request.POST["activity_name"]
            activity_city = request.POST["activity_city"]
            activity_date = request.POST["activity_date"]
            activity_time = request.POST["activity_time"]
            activity_price = request.POST["activity_price"]
            if not activity_price:
                activity_price = 0
            else:
                activity_price = float(activity_price)
            activity_notes = request.POST["activity_notes"]
            activity_image = request.POST["activity_image"]
            activity_date_time = datetime.strptime(f"{activity_date} {activity_time}", "%Y-%m-%d %H:%M")

            edit_activity = Activity.objects.get(id=id)
            edit_activity.title = activity_name
            edit_activity.activity_date_time = activity_date_time
            edit_activity.city = activity_city
            edit_activity.price = activity_price
            edit_activity.description = activity_notes
            edit_activity.image = activity_image
            edit_activity.save()
        
        elif category == "Restaurant":
            restaurant_name = request.POST["restaurant_name"]
            restaurant_city = request.POST["restaurant_city"]
            restaurant_date = request.POST["restaurant_date"]
            restaurant_time = request.POST["restaurant_time"]
            restaurant_price = request.POST["restaurant_price"]
            if not restaurant_price:
                restaurant_price = 0
            else:
                restaurant_price = float(restaurant_price)
            restaurant_note = request.POST["restaurant_notes"]
            restaurant_image = request.POST["restaurant_image"]
            restaurant_date_time = datetime.strptime(f"{restaurant_date} {restaurant_time}", "%Y-%m-%d %H:%M")

            edit_restaurant = Restaurant.objects.get(id=id)
            edit_restaurant.restaurant_name = restaurant_name
            edit_restaurant.city = restaurant_city
            edit_restaurant.price = restaurant_price
            edit_restaurant.notes = restaurant_note
            edit_restaurant.image = restaurant_image
            edit_restaurant.restaurant_date_time = restaurant_date_time
            edit_restaurant.save()



        return HttpResponseRedirect(reverse("activity_details",args=[category,id]))


def edit_trip(request, id):
    if request.method == "GET":
        try:

            user_trips = Trip.objects.get(id=id, user=request.user) 

            return render(request, "trip_planner/edit_trip.html", {
                "user_trip": user_trips 
            })
        except Trip.DoesNotExist:
            
            return HttpResponseRedirect(reverse("index"))
    else:
        title = request.POST["trip_title"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        
        edit_unique_trip = Trip.objects.get(id=id)
        edit_unique_trip.title = title
        edit_unique_trip.start_date = start_date
        edit_unique_trip.end_date = end_date
        
        if "image" in request.FILES:
                edit_unique_trip.image = request.FILES["image"]


        edit_unique_trip.save()

    return HttpResponseRedirect(reverse("index"))

    

    