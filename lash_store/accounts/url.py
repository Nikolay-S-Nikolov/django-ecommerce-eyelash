from django.urls import path, include

from lash_store.accounts.views import ProfileDetailsView, ProfileEditView

urlpatterns = [
    path('', ProfileDetailsView.as_view(), name='profile_details'),
    path('edit/', ProfileEditView.as_view(), name='edit_profile'),
]
