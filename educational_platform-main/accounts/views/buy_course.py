from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from ..models import Course, CourseTopic, Lesson
from ..forms import CourseForm, CourseStructureForm
from ..decorators import editor_required
import json


def buy_course(request):
    return render(request, 'accounts/course_buy.html')
