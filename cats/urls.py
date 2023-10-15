from django.urls import path

from . import views

app_name = "cats"
urlpatterns = [
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/adopted", views.AdoptedDetailView.as_view() , name="adopted_detail")
]
