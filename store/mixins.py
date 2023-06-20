from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class CustomerRequiredMixin(LoginRequiredMixin):
    """
    customer required mixin checks if user is customer or not
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_customer:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied
