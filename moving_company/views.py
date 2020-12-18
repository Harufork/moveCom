from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from additional_functions import UserIsStaff, get_cls_verbose_name_plural, get_lower_name_cls, \
    get_abstract_url_for_navigation
from orders.models import MoveAssistanceRequest, MoveRequest, MoveOrder, \
    EmployeeForMove, TransportForMove, PackingForMove, RouteMove, \
    EmployeeForMoveRequest, TransportForMoveRequest
from packing.models import TypePacking, Measurement, Packing
from transport.models import ModeTransport, Transport
from pricelist.models import PriceRole, PriceModeTransport, \
    PriceModeTDistance, PricePacking
from users.models import EmployeeRole, Profile, Employee
from django.urls import reverse
from django.contrib.auth.models import User, Group

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
            'title': 'Навигация',
            'verbose': {},
            'applications': {}
        }

        line_break = False
        for appkey, appval in {
            'Заказы': ("orders", [MoveAssistanceRequest, True, MoveRequest, EmployeeForMoveRequest,
                                  TransportForMoveRequest, PackingForMove, RouteMove, True, MoveOrder,
                                  EmployeeForMove, TransportForMove]),
            'Упаковка': ("packing", [Packing, Measurement, TypePacking]),
            'Транспорт': ("transport", [ModeTransport, Transport]),
            'Прайс-листы': ("pricelist", [PriceRole, PriceModeTransport, PriceModeTDistance, PricePacking]),
            'Пользователи': ("users", [EmployeeRole, Profile, Employee, Group, User])
        }.items():
            context['applications'][appkey] = []
            for cls in appval[1]:
                if cls is True:
                    line_break = True
                    continue
                cls_name = get_lower_name_cls(cls)
                change_perm = request.user.has_perm(appval[0] + ".change_" + cls_name)
                if request.user.has_perm(appval[0] + ".view_" + cls_name) or change_perm:
                    context['applications'][appkey].append({'verbose': get_cls_verbose_name_plural(cls),
                                                            'change_perm': change_perm,
                                                            'url': get_abstract_url_for_navigation(cls_name),
                                                            'line_break': line_break
                                                            })
                    line_break = False
            if len(context['applications'][appkey]) == 0:
                del context['applications'][appkey]
        return render(request, 'moving_company/navigation.html', context=context)
