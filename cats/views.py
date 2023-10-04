from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.db.models import Q

from .models import Cat

class DetailView(generic.DetailView):
    model = Cat
    template_name = "cats/detail.html"

    def get_queryset(self):
        return Cat.objects.exclude(is_adopted=True).all()