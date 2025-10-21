from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ..models import Lesson, LessonContent, OpenAnswerAttempt, UserAnswer
import json

@login_required
def edit_lesson_content(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    content = lesson.contents.all()
    return render(request, 'accounts/edit_lesson_content.html', {
        'lesson': lesson,
        'content': content
    })

@csrf_exempt
@login_required
def save_lesson_content(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            blocks = data.get('blocks', [])
            # Удаляем старое содержимое
            lesson.contents.all().delete()
            # Сохраняем новые блоки
            for block in blocks:
                block_type = block.get('type')
                block_data = block.get('data', {})
                if block_type == 'text':
                    LessonContent.objects.create(
                        lesson=lesson,
                        content_type='text',
                        text=block_data.get('text', ''),
                    )
                elif block_type == 'pdf':
                    LessonContent.objects.create(
                        lesson=lesson,
                        content_type='pdf',
                        pdf_title=block_data.get('title', ''),
                        pdf_file=block_data.get('file', ''),
                    )
                elif block_type == 'video':
                    LessonContent.objects.create(
                        lesson=lesson,
                        content_type='video',
                        video_title=block_data.get('title', ''),
                        video_url=block_data.get('url', ''),
                        video_description=block_data.get('description', ''),
                    )
                elif block_type in ['test', 'quiz']:
                    LessonContent.objects.create(
                        lesson=lesson,
                        content_type='quiz',
                        quiz_title=block_data.get('title', ''),
                        quiz_question=block_data.get('question', ''),
                        quiz_options=block_data.get('options', []),
                        quiz_correct_answer=block_data.get('correctAnswer', ''),
                        quiz_explanation=block_data.get('explanation', ''),
                    )
                elif block_type == 'task':
                    LessonContent.objects.create(
                        lesson=lesson,
                        content_type='task',
                        task_title=block_data.get('title', ''),
                        task_description=block_data.get('description', ''),
                        task_image=block_data.get('image', ''),
                        task_image_description=block_data.get('imageDescription', ''),
                        task_answer_type=block_data.get('answerType', ''),
                        task_correct_answer=block_data.get('correctAnswer', ''),
                        task_hint=block_data.get('hint', ''),
                    )
                # Можно добавить обработку других типов блоков при необходимости
                else:
                    continue
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Метод не поддерживается'}, status=400)

@csrf_exempt
def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        from ..models import LessonContent, Lesson
        lesson_id = request.POST.get('lesson_id')
        lesson = Lesson.objects.get(id=lesson_id)
        content = LessonContent.objects.create(
            lesson=lesson,
            content_type='pdf',
            pdf_file=pdf_file
        )
        return JsonResponse({
            'success': True,
            'file_url': content.pdf_file.url,
            'file_name': content.pdf_file.name,
            'file_size': content.pdf_file.size
        })
    return JsonResponse({
        'success': False,
        'error': 'No PDF file uploaded'
    }, status=400)

@csrf_exempt
def upload_task_image(request):
    if request.method == 'POST' and request.FILES.get('image_file'):
        image_file = request.FILES['image_file']
        from ..models import LessonContent, Lesson
        lesson_id = request.POST.get('lesson_id')
        lesson = Lesson.objects.get(id=lesson_id)
        content = LessonContent.objects.create(
            lesson=lesson,
            content_type='task',
            task_image=image_file
        )
        return JsonResponse({
            'success': True,
            'file_url': content.task_image.url,
            'file_name': content.task_image.name,
            'file_size': content.task_image.size
        })
    return JsonResponse({
        'success': False,
        'error': 'No image file uploaded'
    }, status=400)

@csrf_exempt
@login_required
def save_task_answer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            block_id = data.get('block_id')
            answer = data.get('answer')

            content = get_object_or_404(LessonContent, id=block_id)
            if content.content_type != 'task':
                return JsonResponse({'success': False, 'error': 'Неверный тип блока'}, status=400)

            # Создаем или обновляем ответ пользователя
            user_answer, created = UserAnswer.objects.update_or_create(
                user=request.user,
                content=content,
                defaults={'answer': answer}
            )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Метод не поддерживается'}, status=400)

@csrf_exempt
@login_required
def save_quiz_answer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            block_id = data.get('block_id')
            answer = data.get('answer')
            is_correct = data.get('is_correct')

            content = get_object_or_404(LessonContent, id=block_id)
            if content.content_type != 'quiz':
                return JsonResponse({'success': False, 'error': 'Неверный тип блока'}, status=400)

            # Создаем или обновляем ответ пользователя
            user_answer, created = UserAnswer.objects.update_or_create(
                user=request.user,
                content=content,
                defaults={
                    'answer': answer,
                    'is_correct': is_correct
                }
            )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Метод не поддерживается'}, status=400)