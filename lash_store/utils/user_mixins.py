from lash_store.accounts.models import Profile

class GetProfileIdMixin:
    def get_object(self, queryset=None):
        pk = self.request.user.pk
        return Profile.objects.get(user_id=pk)