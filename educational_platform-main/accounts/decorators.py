from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps

def editor_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_editor or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return redirect('access_denied')
    return _wrapped_view 