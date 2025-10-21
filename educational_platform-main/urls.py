from django.urls import path
from . import views

urlpatterns = [
    # ... existing urls ...
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('api/save-answer/', views.save_answer, name='save_answer'),
    path('api/save-grades/', views.save_grades, name='save_grades'),
] 