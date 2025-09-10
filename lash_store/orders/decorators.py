from functools import wraps
from django.http import JsonResponse
from django.urls import reverse

def ajax_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = reverse('account_login')
            return JsonResponse({
                "success": False,
                "redirect": login_url,
                "message": "Трябва да сте логнати, за да извършите това действие."
            })
        return view_func(request, *args, **kwargs)
    return _wrapped_view