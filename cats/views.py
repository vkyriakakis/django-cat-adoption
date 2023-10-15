from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cat
from adopt.models import AdoptionRequest

class DetailView(generic.DetailView):
    model = Cat
    template_name = "cats/detail.html"

    def get_queryset(self):
        return Cat.objects.exclude(is_adopted=True).all()

class AdoptedDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cat
    template_name = "cats/adopted.html"

    def get_queryset(self):
        return Cat.objects.filter(adoptionrequest__user=self.request.user,
                                  adoptionrequest__status=AdoptionRequest.Status.APPROVED)