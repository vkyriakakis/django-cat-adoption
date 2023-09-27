from django.views import generic

from cats.models import Cat

class IndexView(generic.ListView):
    model = Cat
    template_name = "index.html"

    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.all()[:9]
