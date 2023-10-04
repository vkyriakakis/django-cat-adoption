from django.views import generic

from cats.models import Cat

class IndexView(generic.ListView):
    model = Cat
    template_name = "index.html"

    def get_queryset(self):
        return Cat.objects.exclude(is_adopted=True).all()
