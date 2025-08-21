from django.shortcuts import render
from django.views import generic as views
# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Начална страница")


class IndexView(views.TemplateView):
    template_name = 'base.html'