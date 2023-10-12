from django.views import generic

from cats.models import Cat

class IndexView(generic.ListView):
    model = Cat
    template_name = "index.html"

    def get_queryset(self):
        # Show only the first 8 cats, so that the adoptee
        # will get a small taste in the index
        return Cat.objects.exclude(is_adopted=True).all()[:8]
