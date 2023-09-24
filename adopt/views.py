from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Cat

class IndexView(generic.ListView):
    model = Cat
    template_name = "adopt/index.html"

    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.all()[:9]


class DetailView(generic.DetailView):
    model = Cat
    template_name = "adopt/detail.html"