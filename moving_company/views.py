from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from additional_functions import UserIsStaff

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        """Формирование домашней страницы сайта"""
        context = {
            'title': 'Время переезда'
        }
        return render(request, 'moving_company/home.html', context=context)


class FaqView(View):
    def get(self, request, *args, **kwargs):
        """Формирование FAQ страницы сайта"""
        context = {
            'title': 'FAQ'
        }
        return render(request, 'moving_company/faq.html', context=context)


class NavigationView(LoginRequiredMixin, UserIsStaff, View):
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Время переезда'
        }
        return render(request, 'moving_company/navigation.html', context=context)