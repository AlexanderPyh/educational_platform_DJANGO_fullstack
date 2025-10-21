from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
@require_POST
@csrf_exempt
def save_answer(request):
    try:
        data = json.loads(request.body)
        block_id = data.get('block_id')
        block_type = data.get('block_type')
        answer = data.get('answer')

        if not all([block_id, block_type, answer]):
            return JsonResponse({'success': False, 'error': 'Не все необходимые данные предоставлены'})

        # Получаем или создаем прогресс урока
        lesson = ContentBlock.objects.get(id=block_id).lesson
        progress, created = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )

        # Сохраняем ответ в зависимости от типа блока
        if block_type == 'open':
            question = OpenQuestion.objects.get(id=block_id)
            answer_obj, created = OpenQuestionAnswer.objects.get_or_create(
                user=request.user,
                question=question,
                defaults={'answer': answer}
            )
            if not created:
                answer_obj.answer = answer
                answer_obj.save()

        # Обновляем прогресс
        progress.update_progress(block_id)
        current_progress = progress.calculate_progress()

        return JsonResponse({
            'success': True,
            'progress': current_progress
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
@csrf_exempt
def save_grades(request):
    try:
        data = json.loads(request.body)
        block_id = data.get('block_id')
        grades = data.get('grades')

        if not all([block_id, grades]):
            return JsonResponse({'success': False, 'error': 'Не все необходимые данные предоставлены'})

        # Проверяем, является ли пользователь преподавателем
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

        # Получаем ответ и обновляем оценки
        question = OpenQuestion.objects.get(id=block_id)
        answer = OpenQuestionAnswer.objects.get(question=question)
        
        # Валидация оценок
        max_scores = {criterion['id']: criterion['points'] for criterion in question.criteria}
        for criterion_id, score in grades.items():
            if score > max_scores.get(criterion_id, 0):
                return JsonResponse({
                    'success': False,
                    'error': f'Оценка превышает максимально возможную для критерия {criterion_id}'
                })

        answer.grades = grades
        answer.is_graded = True
        answer.save()

        # Обновляем общий прогресс урока
        progress = LessonProgress.objects.get(user=answer.user, lesson=question.lesson)
        progress.total_score = answer.calculate_total_score()
        progress.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress = LessonProgress.objects.filter(user=request.user, lesson=lesson).first()
    
    # Получаем предыдущий и следующий уроки
    previous_lesson = Lesson.objects.filter(
        topic=lesson.topic,
        order__lt=lesson.order
    ).order_by('-order').first()
    
    next_lesson = Lesson.objects.filter(
        topic=lesson.topic,
        order__gt=lesson.order
    ).order_by('order').first()

    # Получаем сохраненные ответы пользователя
    user_answers = {}
    if request.user.is_authenticated:
        for block in lesson.content_blocks.all():
            if block.content_type == 'open':
                answer = OpenQuestionAnswer.objects.filter(
                    user=request.user,
                    question_id=block.id
                ).first()
                if answer:
                    user_answers[block.id] = answer.answer

    context = {
        'lesson': lesson,
        'progress_percent': progress.calculate_progress() if progress else 0,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
        'user_answers': user_answers,
        'is_teacher': request.user.is_staff
    }
    
    return render(request, 'accounts/step3_user.html', context) 