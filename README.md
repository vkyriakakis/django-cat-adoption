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

Staff members can login to the admin page (localhost:8000/admin) and 
perform most administrative actions.



## Admin-side
