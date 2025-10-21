#Представления для страницы личного кабинета
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from ..models import Lesson, LessonContent, PurchasedLesson, UserToken


@login_required
def personal_page(request):
    return render(request, 'accounts/personal_page.html')

