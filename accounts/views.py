from django.views.generic.edit import CreateView
from .forms import RegistrationForm
from django.urls import reverse_lazy
from django.shortcuts import render

class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "registration/registration.html"
    success_url = reverse_lazy("registration_done")

def registration_done(request):
    return render(request, "registration/registration_complete.html")