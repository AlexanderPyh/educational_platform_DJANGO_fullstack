from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from ..models import Lesson, LessonContent, PurchasedLesson, UserToken

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    is_purchased = PurchasedLesson.objects.filter(
        user=request.user,
        lesson=lesson
    ).exists()
    
    return render(request, 'accounts/lesson_detail.html', {
        'lesson': lesson,
        'is_purchased': is_purchased
    })

@login_required
def lesson_content(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    content = lesson.contents.all()
    is_purchased = PurchasedLesson.objects.filter(
        user=request.user,
        lesson=lesson
    ).exists()
    
    return render(request, 'accounts/lesson_content.html', {
        'lesson': lesson,
        'content': content,
        'is_purchased': is_purchased
    })

@ensure_csrf_cookie
@require_POST
@login_required
def purchase_lesson(request, lesson_id):
    try:
        lesson = get_object_or_404(Lesson, id=lesson_id)
        user_token = request.user.tokens
        
        if user_token.balance >= lesson.price_in_tokens:
            user_token.balance -= lesson.price_in_tokens
            user_token.save()
            
            PurchasedLesson.objects.create(
                user=request.user,
                lesson=lesson
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Урок успешно куплен',
                'new_balance': float(user_token.balance)
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Недостаточно токенов'
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
def step3_user(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)


    is_purchased = PurchasedLesson.objects.filter(
        user=request.user,
        lesson=lesson
    ).exists()


    is_course_editor = (lesson.topic.course.editor == request.user)


    if not is_purchased and not is_course_editor:
        return redirect('login', lesson_id=lesson_id)


    contents = LessonContent.objects.filter(lesson=lesson).order_by('order')

    return render(request, 'accounts/step3_user.html', {
        'lesson': lesson,
        'contents': contents
    }) 