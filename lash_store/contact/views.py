from django.http import JsonResponse
from django.views import generic as views
from django.views.decorators.http import require_POST
from django.core.mail import send_mail

from lash_store.contact.forms import ContactForm
from lash_store.contact.models import ContactInfo, SocialLink
from lash_store.settings import EMAIL_HOST_USER


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
        context['links'] = SocialLink.objects.order_by('appearance_order', 'label')
        return context

contact_page = ContactPageView.as_view()

@require_POST
def send_contact_message(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        subject = f'Ново съобщение от {name} ({email})'
        email_message = f'Име: {name}\nEmail: {email}\nСъобщение:\n{message}'
        send_mail(subject,message =email_message,from_email=email,recipient_list = [EMAIL_HOST_USER],fail_silently=False)
        return JsonResponse({'success': True, 'message': 'Съобщението е изпратено успешно!'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})