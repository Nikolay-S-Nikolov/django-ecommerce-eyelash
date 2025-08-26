from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic as views

from lash_store.accounts.models import Profile
from lash_store.utils.user_mixins import GetProfileIdMixin

User_model = get_user_model()

class ProfileDetailsView(LoginRequiredMixin, GetProfileIdMixin, views.DetailView):
    template_name = 'accounts/profile_details.html'
    model = Profile
    context_object_name = 'profile'


class ProfileEditView(LoginRequiredMixin, GetProfileIdMixin, views.UpdateView):
    template_name = 'accounts/profile_edit.html'
    model = Profile
    context_object_name = 'profile'
    fields = (
        'preferred_name_nickname',
        'phone_number',
        'profile_picture',
    )
    success_url = reverse_lazy('profile_details')
    
