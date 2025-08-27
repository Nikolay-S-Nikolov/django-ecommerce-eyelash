from lash_store.accounts.models import Profile

class GetProfileIdMixin:
    def get_object(self, queryset=None):
        return Profile.objects.select_related('user').get(user=self.request.user)