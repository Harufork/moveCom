from django.shortcuts import render
from django.views import View


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        """Формирование домашней страницы сайта"""
        context = {
            'title': 'Время переезда'
        }
        return render(request, 'home.html', context=context)
