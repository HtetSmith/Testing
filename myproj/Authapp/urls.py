from django.urls import path
from .views import DashboardView, InstructorView, HRDashboardView
urlpatterns = [
    path('', HRDashboardView.as_view(), name='student_dashboard'),
    path('admin_dashboard/', DashboardView.as_view(), name='admin_dashboard'),
    path('instructor_dashboard/', InstructorView.as_view(), name='instructor_dashboard'),
]