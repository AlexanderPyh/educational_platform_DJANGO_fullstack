from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    UserProfile,
    UserToken,
    Course,
    CourseTopic,
    Lesson,
    LessonContent,
    PurchasedLesson,
    LessonProgress,
)

# Регистрируем кастомную модель пользователя с настройками отображения
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'phone', 'year', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'year')
    search_fields = ('email', 'username', 'phone')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone', 'year', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Роли', {'fields': ('is_editor',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'year', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )

# Регистрируем профиль пользователя
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "get_balance", "telegram_id")
    search_fields = ("user__username", "telegram_id")

    @admin.display(description="Баланс токенов")
    def get_balance(self, obj):
        return obj.user.tokens.balance if hasattr(obj.user, 'tokens') else 0

# Регистрируем токены пользователя
@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "balance")
    search_fields = ("user__email",)


# Регистрируем курсы
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'level', 'editor', 'is_draft', 'is_approved')
    list_filter = ('subject', 'level', 'is_draft', 'is_approved')
    search_fields = ('title', 'description', 'tags')
    ordering = ('title',)

# Регистрируем темы курса
@admin.register(CourseTopic)
class CourseTopicAdmin(admin.ModelAdmin):
    list_display = ('course', 'title')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    ordering = ('title',)

# Регистрируем уроки
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'price_in_tokens')
    list_filter = ('topic',)
    search_fields = ('title', 'topic__title')
    ordering = ('topic__title', 'title')

# Регистрируем содержимое урока
@admin.register(LessonContent)
class LessonContentAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'get_content_type', '__str__')
    list_filter = ('content_type', 'lesson')
    search_fields = (
        'lesson__title',
        'text',
        'pdf_title',
        'video_title',
        'quiz_question',
        'task_title'
    )
    ordering = ('lesson',)

    def get_content_type(self, obj):
        return obj.get_content_type_display()
    get_content_type.short_description = 'Тип содержимого'

# Регистрируем купленные уроки
@admin.register(PurchasedLesson)
class PurchasedLessonAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'purchased_at')
    list_filter = ('purchased_at', 'user', 'lesson')
    search_fields = ('user__email', 'lesson__title')
    ordering = ('-purchased_at',)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'total_score', 'is_completed', 'last_accessed')
    list_filter = ('is_completed', 'last_accessed')
    search_fields = ('user__email', 'lesson__title')
    raw_id_fields = ('user', 'lesson')
