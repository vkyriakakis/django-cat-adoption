from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from django.utils import timezone
from functools import reduce

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
        ages = list(map(Cat.get_internal_age, self.request.GET.getlist("age")))
        sexes = list(map(Cat.get_internal_sex, self.request.GET.getlist("sex")))
        colors = list(map(Cat.get_internal_color, self.request.GET.getlist("color")))

        is_vaccinated = self.request.GET.get("vaccinated") 
        is_house_trained = self.request.GET.get("house_trained")
        is_sterilized = self.request.GET.get("sterilized")

        object_list = Cat.objects

        # Don't apply a multiple choice filter if no choices or all choices are selected
        if ages and len(ages) != len(Cat.Age.values):
            # Compose an OR expression because many values might be provided for that field
            ages_q = [Q(age=age) for age in ages]
            ages_or = ages_q[0]
            for age_q in ages_q[1:]:
                ages_or |= age_q

            object_list = object_list.filter(ages_or)

        if sexes and len(sexes) != len(Cat.Sex.values):
            sexes_q = [Q(sex=sex) for sex in sexes]
            sexes_or = sexes_q[0]
            for sex_q in sexes_q[1:]:
                sexes_or |= sex_q
                
            object_list = object_list.filter(sexes_or)

        if colors and len(colors) != len(Cat.Color.values):
            colors_q = [Q(color=color) for color in colors]
            colors_or = colors_q[0]
            for color_q in colors_q[1:]:
                colors_or |= color_q
                
            object_list = object_list.filter(colors_or)

        if is_vaccinated == "true":
            object_list = object_list.filter(is_vaccinated=True)

        if is_house_trained == "true":
            object_list = object_list.filter(is_house_trained=True)

        if is_sterilized == "true":
            object_list = object_list.filter(is_sterilized=True)

        return object_list.all()