from django.views import generic as views

from lash_store.contact.forms import ContactForm
from lash_store.contact.models import ContactInfo, SocialLink


class ContactPageView(views.FormView):
    template_name = 'contact/contact_page.html'
    form_class = ContactForm

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial.update({
                'email': self.request.user.email,
                'phone': self.request.user.profile.phone_number
            })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInfo.objects.filter(visible=True).order_by('-updated_at').first()
        context['links'] = SocialLink.objects.order_by('-appearance_order', 'label')
        return context

contact_page = ContactPageView.as_view()