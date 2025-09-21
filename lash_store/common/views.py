from django.views import generic as views

class IndexView(views.TemplateView):
    template_name = 'index.html'

index_view = IndexView.as_view()

class AboutView(views.TemplateView):
    template_name = 'about/about.html'

about_view = AboutView.as_view()