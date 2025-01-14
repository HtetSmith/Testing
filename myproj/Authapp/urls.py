from django.urls import path
from .views import DashboardView, InstructorView, HRDashboardView, PostListView, PostUpdateView, PostDetailView, PostCreateView, PostDeleteView
urlpatterns = [
    path('', HRDashboardView.as_view(), name='student_dashboard'),
    path('admin_dashboard/', DashboardView.as_view(), name='admin_dashboard'),
    path('instructor_dashboard/', InstructorView.as_view(), name='instructor_dashboard'),

    # Course URLs

    path('courses/', PostListView.as_view(), name='post_list'),
    path('courses/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('courses/add/', PostCreateView.as_view(), name='post_create'),
    path('courses/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('courses/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # Quiz URLs
    # path('quizzes/add/', views.add_quiz, name='add_quiz'),
    # path('quizzes/<int:quiz_id>/edit/', views.update_quiz, name='update_quiz'),
    # path('quizzes/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
]