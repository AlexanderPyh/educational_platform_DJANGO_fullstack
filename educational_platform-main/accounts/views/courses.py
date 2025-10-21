from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from ..models import Course, CourseTopic, Lesson
from ..forms import CourseForm, CourseStructureForm
from ..decorators import editor_required
import json

@login_required
def course_list_superuser(request):
    courses = Course.objects.all()
    return render(request, 'accounts/course_list_superuser.html', {'courses': courses})

@editor_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.editor = request.user
            course.is_draft = False
            course.is_approved = True
            course.save()
            request.session['course_id'] = course.id
            return redirect('step2')
        else:
            return render(request, 'accounts/step1.html', {'form': form})
    else:
        form = CourseForm()
    return render(request, 'accounts/step1.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    return redirect('course_list_superuser')

@editor_required
def save_course_structure(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Метод не поддерживается'})
    
    course_id = request.session.get('course_id')
    if not course_id:
        return JsonResponse({'success': False, 'error': 'Курс не найден'})
    
    try:
        course = Course.objects.get(id=course_id)
        data = json.loads(request.body)
        
        # Удаляем существующие темы и уроки
        CourseTopic.objects.filter(course=course).delete()
        
        # Сохраняем темы
        for topic_data in data.get('topics', []):
            topic = CourseTopic.objects.create(
                course=course,
                title=topic_data['title']
            )
            
            # Сохраняем уроки для темы
            for lesson_data in topic_data.get('lessons', []):
                Lesson.objects.create(
                    topic=topic,
                    title=lesson_data['title'],
                    price_in_tokens=lesson_data['price']
                )
        
        return JsonResponse({
            'success': True
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': str(e)
        })

@editor_required
def step2(request):
    course_id = request.session.get('course_id')
    if not course_id:
        return redirect('create_course')
    
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = CourseStructureForm(request.POST)
        if form.is_valid():
            # Сохраняем структуру курса
            save_course_structure(request)
            return redirect('course_list_superuser')
    else:
        form = CourseStructureForm()
    
    return render(request, 'accounts/step2.html', {
        'form': form,
        'course': course
    })

@login_required
def course_detail_user(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    topics = course.topics.all().order_by('order')
    
    # Получаем список ID купленных уроков
    purchased_lessons = request.user.purchased_lessons.values_list('lesson_id', flat=True)
    
    return render(request, 'accounts/step2_user.html', {
        'course': course,
        'topics': topics,
        'purchased_lessons': [str(lesson_id) for lesson_id in purchased_lessons]
    })

@editor_required
def step3(request):
    course_id = request.session.get('course_id')
    if not course_id:
        return redirect('create_course')
    
    course = get_object_or_404(Course, id=course_id)
    topics = course.topics.all()
    
    return render(request, 'accounts/step3.html', {
        'course': course,
        'topics': topics
    }) 