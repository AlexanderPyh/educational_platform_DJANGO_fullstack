from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import JSONField

# --------------------------------------
# 👤 Кастомная модель пользователя
# --------------------------------------
class CustomUser(AbstractUser):
    """
    Кастомный пользователь с авторизацией по email.
    Email уникален и используется как основной логин.
    """
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, unique=True, verbose_name="Телефон")
    year = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Год рождения")
    is_editor = models.BooleanField(default=False, verbose_name="Редактор")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

# --------------------------------------
# 📄 Профиль пользователя (роль, телеграм, баланс)
# --------------------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="profile"
    )
    telegram_id = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Telegram ID"
    )

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

# --------------------------------------
# 💰 Токены пользователя
# --------------------------------------
class UserToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tokens',
        verbose_name="Пользователь"
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Баланс токенов"
    )

    def __str__(self):
        return f"{self.user.email} — {self.balance} токенов"

    class Meta:
        verbose_name = "Токены пользователя"
        verbose_name_plural = "Токены пользователей"

# --------------------------------------
# 🔔 Сигналы: автосоздание профиля и токенов
# --------------------------------------
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_and_tokens(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        UserToken.objects.create(user=instance)

# --------------------------------------
# 💸 История покупок токенов
# --------------------------------------
class TokenPurchase(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='token_purchases',
        verbose_name="Пользователь"
    )
    amount = models.PositiveIntegerField(verbose_name="Количество токенов")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата покупки")

    def __str__(self):
        return f"{self.user.email} - {self.amount} токенов за {self.price}₽"

    class Meta:
        verbose_name = "Покупка токенов"
        verbose_name_plural = "Покупки токенов"
        ordering = ['-purchased_at']

# Существующие модели (без изменений)
class Course(models.Model):
    SUBJECT_CHOICES = [
        ('math', 'Математика'),
        ('eco', 'Экономика'),
        ('phys', 'Физика'),
    ]
    LEVEL_CHOICES = [
        ('easy', 'Лёгкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
        ('advanced', 'Продвинутый'),
    ]
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    tags = models.CharField(max_length=255, help_text="Введите через запятую")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    description = models.TextField(blank=True, null=True)
    is_draft = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)

    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',')]

    def __str__(self):
        return self.title

class CourseTopic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    topic = models.ForeignKey(CourseTopic, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    price_in_tokens = models.PositiveIntegerField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.topic.title} - {self.title}"

class LessonContent(models.Model):
    lesson = models.ForeignKey(
        'Lesson',
        on_delete=models.CASCADE,
        related_name='contents'
    )
    order = models.PositiveIntegerField(default=0)
    CONTENT_TYPES = [
        ('text', 'Текст'),
        ('pdf', 'PDF'),
        ('video', 'Видео'),
        ('quiz', 'Тест'),
        ('task', 'Задача'),
        ('open', 'Открытый ответ'),
    ]
    content_type = models.CharField(
        max_length=10,
        choices=CONTENT_TYPES
    )
    text = models.TextField(blank=True, null=True)
    pdf_title = models.CharField(max_length=255, blank=True, null=True)
    pdf_file = models.FileField(upload_to='lesson_pdfs/', blank=True, null=True)
    video_title = models.CharField(max_length=255, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    video_description = models.TextField(blank=True, null=True)
    quiz_title = models.CharField(max_length=255, blank=True, null=True)
    quiz_question = models.TextField(blank=True, null=True)
    quiz_options = models.JSONField(blank=True, null=True)
    quiz_explanation = models.TextField(blank=True, null=True)
    quiz_correct_answer = models.CharField(max_length=255, blank=True, null=True)
    task_title = models.CharField(max_length=255, blank=True, null=True)
    task_description = models.TextField(blank=True, null=True)
    task_image = models.ImageField(upload_to='task_images/', blank=True, null=True, help_text="Загрузите изображение для задачи")
    task_image_description = models.TextField(blank=True, null=True)
    TASK_ANSWER_TYPES = [
        ('text', 'Текстовый'),
        ('number', 'Числовой'),
        ('formula', 'Формула'),
    ]
    task_answer_type = models.CharField(
        max_length=20,
        choices=TASK_ANSWER_TYPES,
        blank=True,
        null=True
    )
    task_correct_answer = models.CharField(max_length=255, blank=True, null=True)
    task_hint = models.TextField(blank=True, null=True)
    open_title = models.CharField(max_length=255, blank=True, null=True)
    open_description = models.TextField(blank=True, null=True)
    open_image = models.ImageField(
        upload_to='open_answers/',
        blank=True,
        null=True
    )
    open_criteria = models.JSONField(
        blank=True,
        null=True,
        help_text='Список критериев и баллов, например [{"criterion": "...", "points": 2}, ...]'
    )
    open_max_attempts = models.PositiveIntegerField(
        default=1,
        help_text='Сколько раз пользователь может отправить ответ'
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.lesson.title} — {self.get_content_type_display()}"

class OpenAnswerAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.ForeignKey(LessonContent, on_delete=models.CASCADE)
    answer_text = models.TextField()
    scores = JSONField()
    total_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class PurchasedLesson(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='purchased_lessons'
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.email} - {self.lesson.title}"

class OpenQuestion(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='open_questions/', null=True, blank=True)
    criteria = models.JSONField(default=list, help_text="Список критериев оценки в формате [{'criterion': 'Критерий', 'points': 10}]")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class LessonProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_blocks = models.JSONField(default=list, help_text="Список ID завершенных блоков")
    total_score = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'lesson']

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"

    def calculate_progress(self):
        total_blocks = self.lesson.content_blocks.count()
        if total_blocks == 0:
            return 0
        return round((len(self.completed_blocks) / total_blocks) * 100)

    def update_progress(self, block_id):
        if block_id not in self.completed_blocks:
            self.completed_blocks.append(block_id)
            self.save()
            return True
        return False

class UserAnswer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    content = models.ForeignKey(
        'LessonContent',
        on_delete=models.CASCADE,
        related_name='user_answers'
    )
    answer = models.TextField()
    is_correct = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'content')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.content}"