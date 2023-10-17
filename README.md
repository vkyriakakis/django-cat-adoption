# django-cat-adoption
A toy website where you can adopt cats, made with Django. A large number of unit tests
is also included.

## To visit the website:

1) Run Django's HTTP server (the default port is 8000) using:
```
python manage.py runserver
```

2) Visit the website in localhost:8000

## To run the unit tests
```
python manage.py test
```

## User-side
<img src="screenshots/index.png" style="height:85%;width:85%">

The part of the site intended for ordinary users (adopters) is straightforward
and includes functionality such as:

- Registration & Authentication
<img src="screenshots/register.png" style="height:85%;width:85%">
<img src="screenshots/login.png" style="height:85%;width:85%">

- Searching for cats based on a number of criteria such as age, sex or color
<img src="screenshots/search.png" style="height:85%;width:85%">

- Viewing the details page for a cat and placing an adoption request (via the "Adopt" button)
<img src="screenshots/details.png" style="height:85%;width:85%">

- Viewing the adoption requests, which might be pending, approved or rejected
<img src="screenshots/adoptions.png" style="height:85%;width:85%">

- Viewing a special details page for cat that has been adopted by the user
<img src="screenshots/adopted_details.png" style="height:85%;width:85%">


## Staff-side

Staff users can login to the admin page ```localhost:8000/admin``` and 
perform most administrative actions. You can use the premade staff user
with the credentials:
```
Username: bot
Password: abojus112
```
to test these functions yourself.

<img src="screenshots/staff_overview.png" style="height:85%;width:85%">

A staff user can:

- Add a new cat
<img src="screenshots/add_cat.png" style="height:85%;width:85%">

- Change the status of an adoption request from pending to approved or rejected (once
an adoption request for a cat by a user is approved, all other requests for the same
cat are rejected automatically)
<img src="screenshots/adoption_requests.png" style="height:85%;width:85%">
<img src="screenshots/change_request_status.png" style="height:85%;width:85%">

## Admin-side

The admin user has the credentials:
```
Username: admin
Password: admin
```
and can do everything the staff users can, 
