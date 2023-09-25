from django.urls import path

from . import views

app_name = "adopt"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('search', views.search, name="search"),
    path('search/results', views.SearchResultsView.as_view(), name="search_results"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
]
