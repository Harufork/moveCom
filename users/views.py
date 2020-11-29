from django.shortcuts import render
from django.views import View




class Registration(View):
    def get(self, request, *args, **kwargs):
        """Формирование страницы для регистрация нового пользователя"""
        context = {
            'title': 'Регистрация - Время переезда'
        }
        return render(request, 'home.html', context=context)
