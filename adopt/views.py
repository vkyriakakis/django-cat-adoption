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

def search(request):
    ages = [x[1] for x in Cat.Age.choices]
    sexes = [x[1] for x in Cat.Sex.choices]
    colors = [x[1] for x in Cat.Color.choices]

    context = {"age_choices": ages, "sex_choices": sexes, \
               "color_choices": colors}

    return render(request, "adopt/search.html", context)


class SearchResultsView(generic.ListView):
    model = Cat
    template_name = "adopt/cat_display.html"

    def get_queryset(self):
        age = Cat.get_internal_age(self.request.GET.get("age"))
        sex = Cat.get_internal_sex(self.request.GET.get("sex"))
        color = Cat.get_internal_color(self.request.GET.get("color"))

        is_vaccinated = True if self.request.GET.get("vaccinated") == "true" else False 
        is_house_trained = True if self.request.GET.get("house_trained") == "true" else False 
        is_sterilized = True if self.request.GET.get("sterilized") == "true" else False 

        object_list = Cat.objects.filter(age=age) \
                                 .filter(sex=sex) \
                                 .filter(color=color) \
                                 .filter(is_vaccinated=is_vaccinated) \
                                 .filter(is_house_trained=is_house_trained) \
                                 .filter(is_sterilized=is_sterilized)

        return object_list