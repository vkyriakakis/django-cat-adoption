from django.urls import path

from . import views

app_name = "search"
urlpatterns = [
    path('', views.search, name="search"),
    path('results/', views.SearchResultsView.as_view(), name="results"),
]
