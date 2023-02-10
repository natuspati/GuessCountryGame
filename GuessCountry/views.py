from django.views.generic import TemplateView

from random import randint


# Create your views here.
class IndexView(TemplateView):
    template_name = "GuessCountry/index.html"
    
    def get(self, request, *args, **kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["num"] = randint(0, 100)
        return context
