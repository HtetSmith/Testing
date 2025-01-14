from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.views import View
from django.dispatch import receiver
from Authapp.mixin import RoleRequiredMixin
from django.db.models.signals import post_save
from Authapp.models import CustomUser, UserProfile
from .forms import CustomUserRegistrationForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group


class DashboardView(RoleRequiredMixin, TemplateView):
    
    template_name = 'dashboard.html'
    allowed_roles = ['Admin']  # Only users in these roles can access

class InstructorView(RoleRequiredMixin, TemplateView):
    template_name = 'Instructor_home_page.html'
    allowed_roles = ['Instructor']  # Only users in these roles can access

class HRDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "Home_Page.html"
    allowed_roles = ['Student']


def custom_login_view(request):
    # # next_url = request.GET.get('next', None)
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     # next_url = request.POST.get('next', None)  # Update from POST data  # Store 'next' during form submission
    #     user = authenticate(request, username=username, password=password)

    #     if user is not None:
    #         if user.groups.filter(name__in=['Admin','Instructor', 'Student']).exists():  # Check roles
    #             login(request, user)
    #             # Role-based redirection
    #             if user.groups.filter(name='Admin').exists():
    #                 return redirect(reverse('admin_dashboard'))  # Redirect to Admin dashboard
    #             elif user.groups.filter(name='Instructor').exists():
    #                 return redirect(reverse('instructor_dashboard'))  # Redirect to Instructor dashboard
    #             elif user.groups.filter(name='Student').exists():
    #                 return redirect(reverse('student_dashboard'))  # Redirect to Student dashboard
    #             else:
    #                 messages.error(request, "You do not have the required permissions.")
    #                 return redirect('custom_login_view')
    #         else:
    #             messages.error(request, "You do not have the required permissions.")
    #             return redirect('custom_login_view')
    #     else:
    #         messages.error(request, "Invalid username or password.")
    #         return redirect('custom_login_view')

    # return render(request, 'Login.html')  # Use Django's default login template
    # next_url = request.GET.get('next', None)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user using email
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid email or password. helow")
            return redirect('custom_login_view')
        # next_url = request.POST.get('next', None)  # Update from POST data
        print(f"User: {user.username}, Password: {user.password},")
        user = authenticate(request, username=user.username, password=password)


        if user is not None:
            login(request, user)
            # Debugging print statement to log user information
            print(f"User: {user.username}, Role: {user.role}, Groups: {list(user.groups.values_list('name', flat=True))}")
            # if user.groups.exists():
            #     if user.groups.filter(name='Admin').exists():
            #         return redirect(reverse('admin_dashboard'))
            #     elif user.groups.filter(name='Instructor').exists():
            #         return redirect(reverse('instructor_dashboard'))
            #     elif user.groups.filter(name='Student').exists():
            #         return redirect(reverse('student_dashboard'))
            # Redirect based on role
            if user.role == 'admin':
                return redirect(reverse('admin_dashboard'))
            elif user.role == 'instructor':
                return redirect(reverse('instructor_dashboard'))
            elif user.role == 'student':
                return redirect(reverse('student_dashboard'))
            else:
                messages.error(request, "You do not have the required permissions.")
                return redirect('custom_login_view')
        else:
            messages.error(request, "Invalid email or password. Hellow")
            return render(request, 'Login.html', {'email': email})
        
    return render(request, 'Login.html')




class RegisterView(View):
    def get(self, request):
        user_form = CustomUserRegistrationForm()
        profile_form = UserProfileForm()
        return render(request, 'register.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        user_form = CustomUserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save user
            user = user_form.save(commit=False)
            # Hash the password
            user.set_password(user.password)
            # Update with Hashed password
            user.save()
            print(f"User: {user.username}, Role: {user.role}, Groups: {list(user.groups.values_list('name', flat=True))}")
            # Assign user to the corresponding group based on role
            # Assign user to group based on role
            role = user.role
            print(f"Attempting to assign group for role: {role}")  # Debugging log
            group, created = Group.objects.get_or_create(name=role.capitalize())
            print(f"Group fetched/created: {group}, Created: {created}")  # Debugging log
            user.groups.add(group)
            print(f"Groups after addition: {list(user.groups.values_list('name', flat=True))}")  # Debugging log
            print(f"User: {user.username}, Role: {user.role}, Groups: {list(user.groups.values_list('name', flat=True))}")
            

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_photo' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_photo = request.FILES['profile_photo']

            profile.save()

            messages.success(request, 'Your account has been created successfully!')
            return redirect('custom_login_view') 

        return render(request, 'register.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })
    
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Add custom logout logic here (optional)
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)



