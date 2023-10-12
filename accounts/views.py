from django.views.generic.edit import CreateView
from .forms import RegistrationForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect

class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "accounts/registration.html"
    success_url = reverse_lazy("accounts:registration_done")

def registration_done(request):
    # If the user is logged in redirect them to the home page
    if request.user.is_authenticated:
        return redirect(reverse("index"))

    return render(request, "accounts/registration_complete.html")