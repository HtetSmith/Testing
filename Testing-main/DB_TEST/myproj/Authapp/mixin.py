from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

class RoleRequiredMixin:
    """
    Custom mixin to restrict access to users with specific roles.
    """
    allowed_roles = []  # List of allowed roles/groups

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     # Redirect to login page if user is not authenticated
        #     return redirect('custom_login_view') 
        
        if request.user.groups.exists():  # Check if the user belongs to a group
            user_groups = request.user.groups.values_list('name', flat=True)
            if any(group in self.allowed_roles for group in user_groups):
                return super().dispatch(request, *args, **kwargs)
            
        return HttpResponseForbidden("You do not have permission to access this page.")