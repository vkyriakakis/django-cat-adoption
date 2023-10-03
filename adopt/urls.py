from django.urls import path

from . import views

app_name = "adopt"
urlpatterns = [
    path('', views.MyAdoptionsView.as_view(), name="my_adoptions"),
    path('<int:cat_id>/', views.request_adoption, name="adopt"),
    path('delete/', views.delete_adoption, name="delete_adoption"),
]
