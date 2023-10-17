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

The part of the site intended for ordinary users (adopters) is straightforward
and includes functionality such as:

- Registration & Authentication
- Searching for cats based on a number of criteria such as age, sex or color
- Viewing the details page for a cat
- Placing an adoption request for a cat
- Viewing the adoption requests, which might be pending, approved or rejected
- Viewing a special details page for cat that has been adopted by the user

<img src="screenshots/index.png" height="500px" width="800px">

## Staff-side

## Admin-side
