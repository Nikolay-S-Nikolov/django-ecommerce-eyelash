from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic as views
from lash_store.utils.user_mixins import GetProfileIdMixin

User_model = get_user_model()

class ProfileDetailsView(LoginRequiredMixin,GetProfileIdMixin,views.DetailView):
    template_name = 'accounts/profile_details.html'
    model = User_model

