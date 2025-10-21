from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from ..forms import CustomUserCreationForm, EmailLoginForm

def new_first(request):
    return render(request, 'accounts/new_first.html')

def login_again(request):
    return render(request, 'accounts/login_again.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('page')
        else:
            messages.error(request, f"Ошибка при регистрации: {form.errors}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/registration.html', {'form': form})

def access_denied(request):
    return render(request, 'accounts/access_denied.html')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        print("DEBUG — логинится пользователь:", user)
        print("DEBUG — is_editor:", getattr(user, 'is_editor', 'НЕТ ПОЛЯ'))
        print("DEBUG — is_superuser:", user.is_superuser)
        auth_login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('course_list_superuser') 