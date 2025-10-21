# accounts/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views.auth import register_view, CustomLoginView, new_first, login_again, access_denied
from .views.courses import course_list_superuser, create_course, delete_course, save_course_structure, step2, \
    course_detail_user, step3
from .views.lessons import lesson_content, purchase_lesson, lesson_detail, step3_user
from .views.content import edit_lesson_content, save_lesson_content, upload_pdf, upload_task_image, save_task_answer, \
    save_quiz_answer
from .views.api import save_answer, save_grades
from .views.buy_course import buy_course
from .views.personal_page import personal_page
from .views.clear_token_history import purchase_token, clear_history, get_token_balance, get_purchase_history



urlpatterns = [
    # Главная страница
    path('', new_first, name='page'),

    # Auth URLs
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('new_first/', new_first, name='new_first'),
    path('login_again/', login_again, name='login_again'),
    path('access-denied/', access_denied, name='access_denied'),

    # Course URLs
    path('course_list_superuser/', course_list_superuser, name='course_list_superuser'),
    path('create_course/', create_course, name='create_course'),
    path('delete_course/<int:id>/', delete_course, name='delete_course'),
    path('save_course_structure/', save_course_structure, name='save_course_structure'),
    path('step1/', create_course, name='step1'),
    path('step2/', step2, name='step2'),
    path('step3/', step3, name='step3'),
    path('course/<int:course_id>/', course_detail_user, name='course_detail_user'),

    # Lesson URLs
    # ВАЖНО: step3_user идёт ДО lesson_detail, чтобы маршрут /view/ обрабатывался правильно
    path('lesson/<int:lesson_id>/view/', step3_user, name='step3_user'),  # <-- Перемещён вверх
    path('lesson/<int:lesson_id>/', lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/content/', lesson_content, name='lesson_content'),
    path('purchase_lesson/<int:lesson_id>/', purchase_lesson, name='purchase_lesson'),

    # Content URLs
    path('edit_lesson_content/<int:lesson_id>/', edit_lesson_content, name='edit_lesson_content'),
    path('save_lesson_content/<int:lesson_id>/', save_lesson_content, name='save_lesson_content'),
    path('upload_pdf/', upload_pdf, name='upload_pdf'),
    path('upload_task_image/', upload_task_image, name='upload_task_image'),

    # API URLs
    path('api/save-answer/', save_answer, name='save_answer'),
    path('api/save-grades/', save_grades, name='save_grades'),
    path('api/save-lesson-content/<int:lesson_id>/', save_lesson_content, name='save_lesson_content_api'),
    # <-- Переименован для уникальности
    path('api/save-task-answer/', save_task_answer, name='save_task_answer'),
    path('api/save-quiz-answer/', save_quiz_answer, name='save_quiz_answer'),

    # User Pages and Actions
    path('buy_course/', buy_course, name='buy_course'),
    path('personal_page/', personal_page, name='personal_page'),
    path('api/purchase-token/', purchase_token, name='purchase_token'),
    path('api/clear-history/', clear_history, name='clear_history'),
    path('api/get-token-balance/', get_token_balance, name='get_token_balance'),
    path('api/get-purchase-history/', get_purchase_history, name='get_purchase_history'),

    # Auth URLs (Logout должен быть в конце, но перед app-specific)
    path('logout/', LogoutView.as_view(next_page='page'), name='logout'),
]