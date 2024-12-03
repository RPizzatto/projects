# Trip Planner

## Project Overview
The **Trip Planner** is a web application designed to help users plan and organize their holidays. It provides a platform to log and manage key trip details, such as transportation, accommodations, meals, and activities. The application serves as both a budgeting tool and a journal for users to log what they’ve done during their trips for future reference.  
The **target audience** includes travelers who want an organized and budget-conscious way to plan their trips while keeping a record of their holiday experiences.

---

## Features

### General Site Features
- **Home Page:**
  - Displays a list of upcoming and past trips.
  - Each trip includes a default image and a button to view detailed trip information.
  - If no trips are scheduled, a motivational message encourages users to plan a trip with a "Create New Trip" button.

- **Trip Details:**
  - Displays trip title, start and end dates, and a list of all activities associated with the trip.
  - Includes an "Add New Activity" button for users to log new activities during their trip.

- **Create New Trip:**
  - Allows users to input a trip title, start and end dates, and upload an image to represent the trip.

- **Create New Activity:**
  - Enables users to add specific details about activities, including title, date, category, price, description, and an optional image.

---

## Distinctiveness and Complexity

### Distinctiveness
- The application is not a typical CRUD-based blog or e-commerce platform. Instead, it’s a niche tool tailored to travel planning and budgeting, combining features such as trip management, budgeting, and activity categorization.
- It uniquely integrates features like categorizing trip components (flights, hotels, activities), calculating budgets dynamically, and providing users with a clean UI to track their travel details.

### Complexity
- The project involves multiple interdependent models (**Trip**, **Activity**, **Hotel**, **Flights**, etc.), requiring careful database design to manage relationships between users, trips, and activities.
- Features such as budget calculation for each trip, dynamic data display for upcoming and past trips, and image handling for trip and activity customization add significant functionality.
- The project demonstrates both front-end (**HTML**, **CSS**, **Bootstrap**, **JavaScript**) and back-end (**Django**, **SQLite**) integration.
- Forms with file uploads (e.g., trip and activity images) and data validation showcase added complexity in managing user inputs.

---

## File Structure and Descriptions

### Models
1. **User**: Built-in Django User model, managing authentication and trip ownership.
2. **Category**: Categorizes activities (e.g., "Restaurant", "Activity").
3. **Trip**: Core model representing a user's trip. Includes title, start date, end date, user association, and an optional image.
4. **Activity**: Represents specific activities within a trip, including details like category, price, and description.
5. **Restaurants**: Stores data about the restaurants.
6. **Hotel**: Stores accommodation details, including dates, price, and contact information.
7. **Flights**: Stores flight details, such as departure and arrival times, airline, and reservation codes.

### Templates
- **`trip_planner/layout.html`**: Base template for consistent site structure, including navigation and styling.
- **`trip_planner/index.html`**: Home page template displaying upcoming and past trips.
- **`trip_planner/trip_details.html`**: Page showing details of a specific trip, including activities and the option to add new ones.
- **`trip_planner/activity_details.html`**: Page showing details of a specific activity.
- **`trip_planner/new_trip.html`**: Form template for creating a new trip.
- **`trip_planner/new_activity.html`**: Form template for adding new activities to a trip.
- **`trip_planner/edit_trip.html`**: Form template for editing existing trips.
- **`trip_planner/edit_activity.html`**: Form template for editing existing activities within a trip.

### Views
- **`index(request)`**: Displays the home page with upcoming and past trips.
- **`trip_details(request, id)`**: Displays the details of a specific trip, including its activities.
- **`activity_details(request, id)`**: Displays the details of a specific activity, including its details.
- **`create_trip(request)`**: Handles the creation of new trips.
- **`create_activity(request, id)`**: Handles the addition of new activities to a trip.
- **`edit_trip(request, id)`**: Allows users to edit the details of an existing trip.
- **`edit_activity(request, id)`**: Allows users to edit the details of an existing activity.

---

## How to Run

1. In your terminal, `cd` into the project directory.
2. Run `python manage.py makemigrations project` to make migrations for the auctions app.
3. Run `python manage.py migrate` to apply migrations to your database.
4. Run `python manage.py runserver` to see the website.
