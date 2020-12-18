from django.shortcuts import render, get_object_or_404
from .forms import ForClientMoveRequest
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from .models import MoveAssistanceRequest, MoveRequest, MoveOrder, \
    EmployeeForMove, TransportForMove, PackingForMove, RouteMove, \
    EmployeeForMoveRequest, TransportForMoveRequest
from additional_functions import get_context_for_view_list, get_context_for_detail_view, \
    get_context_for_form_view, get_context_for_delete_view, UserIsStaff
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from transport.models import ModeTransport
from packing.models import TypePacking, Packing
from users.models import EmployeeRole, Employee
from django.contrib.auth.decorators import permission_required
from additional_functions import get_verbose_of_fields_from_class, get_bool_perm_for_user, get_lower_name_cls, \
    get_urls_for_interection
from django.db.models import Q
import datetime

class ThankForOrder(View):
    def get(self, request, *args, **kwargs):
        """Формирование страницы с благодарностью за заказ"""
        context = {
            'title': 'Спасибо за заказ'
        }
        return render(request, 'orders/thank_for_order.html', context=context)


def new_request_move(request):
    """Формированиае формы на оформление перееезда"""
    context = {
        "routs": []
    }

    if request.method == 'POST':
        dont_valid = True
        # Валидация маршрутов
        for num in range(10):
            get_post_a = request.POST.get("point_a" + str(num))
            get_post_b = request.POST.get("point_b" + str(num))
            if get_post_a is None or get_post_b is None:
                break
            if get_post_a != "" or get_post_b != "":
                none_rout_a = True
                if get_post_a == "":
                    none_rout_a = False
                    dont_valid = False
                none_rout_b = True
                if get_post_b == "":
                    none_rout_b = False
                    dont_valid = False
                context["routs"].append((get_post_a, get_post_b, none_rout_a, none_rout_b))
        if len(context["routs"]) == 0:
            context["routs"] = [("", "", False, False)]
            dont_valid = False

        # TODO: Вынести эту валидацию в отдельную процедуру/функцию
        # Валидация персонала
        name_id = 'emp_roles_post'
        context[name_id] = {}
        quan = "quan"
        hird = "hird"
        skey = 'er'
        quanity_nothing = 0
        cls = EmployeeRole
        for key in request.POST:
            if key.startswith(skey):
                value = request.POST.get(key)
                key = key.split('_')
                try:
                    value = int(value)
                    key[2] = int(key[2])
                except ValueError:
                    continue
                if value > 0:
                    # TODO: Поменять здесь на get(pk=key[2])
                    if cls.objects.filter(pk=key[2]).first() is None:
                        continue
                    if key[1] == quan:
                        ant_attr = hird
                    elif key[1] == hird:
                        ant_attr = quan
                    else:
                        continue
                    if key[2] not in context[name_id]:
                        context[name_id].update({key[2]: {key[1]: value}})
                        context[name_id][key[2]].update({ant_attr: ""})
                        quanity_nothing += 1
                    else:
                        context[name_id][key[2]].update({key[1]: value})
                        quanity_nothing -= 1
        if quanity_nothing != 0:
            dont_valid = False
        # TODO: Вынести эту валидацию в отдельную процедуру/функцию, а лучше объединить, чтобы не делать 2 цикла
        # Валидация транспорта
        name_id = 'mode_transport_post'
        context[name_id] = {}
        quan = "quan"
        hird = "hird"
        skey = 'mt'
        quanity_nothing = 0
        cls = ModeTransport
        for key in request.POST:
            if key.startswith(skey):
                value = request.POST.get(key)
                key = key.split('_')
                try:
                    value = int(value)
                    key[2] = int(key[2])
                except ValueError:
                    continue
                if value > 0:
                    # TODO: Поменять здесь на get(pk=key[2])
                    if cls.objects.filter(pk=key[2]).first() is None:
                        continue
                    if key[1] == quan:
                        ant_attr = hird
                    elif key[1] == hird:
                        ant_attr = quan
                    else:
                        continue
                    if key[2] not in context[name_id]:
                        context[name_id].update({key[2]: {key[1]: value}})
                        context[name_id][key[2]].update({ant_attr: ""})
                        quanity_nothing += 1
                    else:
                        context[name_id][key[2]].update({key[1]: value})
                        quanity_nothing -= 1
        if quanity_nothing != 0:
            dont_valid = False
        if len(context[name_id]) == 0:
            dont_valid = False
            context['nothing_mode_transport'] = True

        # Валидация упаковочного материала
        name_id = 'packing_post'
        context[name_id] = {}
        skey = 'p'
        for key in request.POST:
            if key.startswith(skey):
                value = request.POST.get(key)
                key = key.split('_')
                try:
                    value = int(value)
                    key[1] = int(key[1])
                except ValueError:
                    continue
                if value > 0:
                    if Packing.objects.filter(pk=key[1]).first() is None:
                        continue
                    context[name_id].update({key[1]: value})
        # TODO: Валидация времени что она не меньше текущей, когда сегодняшняя дата

        # TODO: Сделать ограничение на максимальное кол-во у объектов
        form = ForClientMoveRequest(request.POST)
        if form.is_valid() and dont_valid:
            # TODO: Вынести отсюда бизнес-логику по классовым методам и тд
            newMR = MoveRequest()
            # статус ставить не надо, так как он определен поумолчанию
            if request.user.is_authenticated:
                newMR.creater = request.user
            else:
                newMR.creater = None
            newMR.full_name = form.cleaned_data.get('full_name')
            newMR.phone_number = form.cleaned_data.get('phone_number')
            newMR.time_type = form.cleaned_data.get('time_type')
            newMR.receiving_packaging = form.cleaned_data.get('receiving_packaging')
            newMR.payment_type = form.cleaned_data.get('payment_type')
            newMR.date_of_completion = form.cleaned_data.get('date_of_completion')
            if newMR.time_type == 'o':
                newMR.time_of_completion = form.cleaned_data.get('time_of_completion')
            newMR.save()

            # TODO: Добавить новые таблицы для отслеживания кол-ва объектов, для анти спавна
            for key, value in context["emp_roles_post"].items():
                newEFM = EmployeeForMoveRequest()
                newEFM.move_request = newMR
                newEFM.group = EmployeeRole.objects.get(pk=key).group
                newEFM.total = value['quan']
                newEFM.hired_hours = value['hird']
                newEFM.save()

            for key, value in context["mode_transport_post"].items():
                newTFM = TransportForMoveRequest()
                newTFM.move_request = newMR
                newTFM.mode_transport = ModeTransport.objects.get(pk=key)
                newTFM.total = value['quan']
                newTFM.hired_hours = value['hird']
                newTFM.save()

            for key, value in context["packing_post"].items():
                newPFM = PackingForMove()
                newPFM.move_request = newMR
                newPFM.packing = Packing.objects.get(pk=key)
                newPFM.total = value
                newPFM.save()

            for rout in context["routs"]:
                newRM = RouteMove()
                newRM.move_request = newMR
                newRM.point_a = rout[0]
                newRM.point_b = rout[1]
                newRM.distance = 0
                newRM.save()

            return HttpResponseRedirect(reverse('thank_for_order'))
        else:
            context['help_text'] = "Необходимо исправить выделенные ошибки"
    else:
        context["routs"].append(("", "", True, True))
        form = ForClientMoveRequest()

    context['type_packings_with_packings'] = \
        {tp.name: Packing.objects.filter(type=tp) for tp in TypePacking.objects.filter(available=True)}
    additional_packing_name = 'Ещё'
    context['type_packings_with_packings'].update(
        {additional_packing_name: Packing.objects.filter(available=True, type=None)})
    if len(context['type_packings_with_packings'][additional_packing_name]) == 0:
        del context['type_packings_with_packings'][additional_packing_name]
    context.update({
        'title': 'Оформление заказа',
        'mvreq_form': form,
        'mode_transports': ModeTransport.objects.filter(available=True),
        'employee_roles': EmployeeRole.objects.filter(available=True, available_in_order=True),
        "routs_count": len(context["routs"])
    })
    return render(request, 'orders/newrequestmove.html', context=context)


@permission_required("orders.cancel_move_order")
def completed_move_order(request):
    """Завершение заказа на переезд"""
    # TODO: Добавить проверку на статус
    if request.method == 'POST':
        value = request.POST.get("ordmoveid")
        if value is None:
            raise Http404

        try:
            mo = MoveOrder.objects.get(pk=value)
        except MoveOrder.DoesNotExist:
            raise Http404
        mo.completed_move_order()
        return HttpResponseRedirect(reverse("moveorder_executor_list"))
    else:
        raise Http404


@permission_required("orders.cancel_move_order")
def in_progress_move_order(request):
    """Начать выполнение заказа на переезд"""
    # TODO: Добавить проверку на статус
    if request.method == 'POST':
        value = request.POST.get("ordmoveid")
        if value is None:
            raise Http404

        try:
            mo = MoveOrder.objects.get(pk=value)
        except MoveOrder.DoesNotExist:
            raise Http404
        mo.in_progress_move_order()
        return HttpResponseRedirect(reverse("moveorder_executor_view", args=[value]))
    else:
        raise Http404


@permission_required("orders.cancel_move_order")
def cancel_move_order(request):
    """Отмена заказа на переезд"""
    # TODO: Добавить проверку на статус
    if request.method == 'POST':
        value = request.POST.get("ordmoveid")
        if value is None:
            raise Http404

        try:
            mo = MoveOrder.objects.get(pk=value)
        except MoveOrder.DoesNotExist:
            raise Http404
        mo.cancel_move_order()
        return HttpResponseRedirect(mo.get_absolute_url())
    else:
        raise Http404


@permission_required("orders.change_moveorder")
def calc_total_cost_of_move_order(request):
    """Перерасчитать итоговую цену заказа"""
    # TODO: Добавить проверку на статус
    if request.method == 'POST':
        value = request.POST.get("ordmoveid")
        if value is None:
            raise Http404

        try:
            mo = MoveOrder.objects.get(pk=value)
        except MoveOrder.DoesNotExist:
            raise Http404
        mo.calculate_total_cost()
        return HttpResponseRedirect(mo.get_absolute_url())
    else:
        raise Http404


@permission_required("orders.confirm_move_order")
def confirm_move_order(request):
    """Потверждение заказа на переезд"""
    # TODO: Добавить проверку на статус
    if request.method == 'POST':
        value = request.POST.get("ordmoveid")
        if value is None:
            raise Http404

        try:
            mo = MoveOrder.objects.get(pk=value)
        except MoveOrder.DoesNotExist:
            raise Http404
        try:
            mo.confirm_move_order(Employee.objects.get(user=request.user))
        except Employee.DoesNotExist:
            raise Http404
        return HttpResponseRedirect(mo.get_absolute_url())
    else:
        raise Http404


@permission_required("orders.rejection_move_request")
def rejection_move_request(request):
    """Откланение заявки на переезд"""
    # TODO: Добавить проверку на статус
    if request.method == 'POST':
        value = request.POST.get("reqmoveid")
        if value is None:
            raise Http404

        try:
            mr = MoveRequest.objects.get(pk=value)
        except MoveRequest.DoesNotExist:
            raise Http404
        mr.rejection_move_request()
        return HttpResponseRedirect(mr.get_absolute_url())
    else:
        raise Http404


@permission_required("orders.add_moveorder")
def get_move_order_from_request(request):
    """Создать заказ на переезд на основе заявки"""
    # TODO: Добавить проверку на статус
    # TODO: Добавить проверку что у заявки нет заказа
    if request.method == 'POST':
        value = request.POST.get("reqmoveid")
        if value is None:
            raise Http404

        newMO = MoveOrder()

        try:
            newMO.move_request = MoveRequest.objects.get(pk=value)
        except MoveRequest.DoesNotExist:
            raise Http404

        newMO.total_cost = 0
        newMO.save()

        for obj in EmployeeForMoveRequest.objects.filter(move_request=newMO.move_request):
            for i in range(obj.total):
                newEFM = EmployeeForMove()
                newEFM.move_order = newMO
                newEFM.group = obj.group
                newEFM.hired_hours = obj.hired_hours
                newEFM.save()

        for obj in TransportForMoveRequest.objects.filter(move_request=newMO.move_request):
            for i in range(obj.total):
                newTFM = TransportForMove()
                newTFM.move_order = newMO
                newTFM.mode_transport = obj.mode_transport
                newTFM.hired_hours = obj.hired_hours
                newTFM.save()

        newMO.calculate_total_cost()

        return HttpResponseRedirect(newMO.get_absolute_url())
    else:
        raise Http404


class MoveAssistanceRequestViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_moveassistancerequest'
    model = MoveAssistanceRequest
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            get_context_for_view_list(MoveAssistanceRequest, self.request.user, 'orders', 'status', "date_of_creation",
                                      "full_name"))
        return context


class MoveAssistanceRequestView(LoginRequiredMixin, UserIsStaff,
                                PermissionRequiredMixin, generic.DetailView):
    permission_required = 'orders.view_moveassistancerequest'
    model = MoveAssistanceRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            get_context_for_detail_view(MoveAssistanceRequest, super().get_object(), self.request.user, 'orders'))
        return context


class MoveAssistanceRequestCreate(LoginRequiredMixin, UserIsStaff,
                                  PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'orders.add_moveassistancerequest'
    model = MoveAssistanceRequest
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(MoveAssistanceRequest))
        return context


class MoveAssistanceRequestChange(LoginRequiredMixin, UserIsStaff,
                                  PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'orders.change_moveassistancerequest'
    model = MoveAssistanceRequest
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(MoveAssistanceRequest, super().get_object()))
        return context


class MoveAssistanceRequestDelete(LoginRequiredMixin, UserIsStaff,
                                  PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'orders.delete_moveassistancerequest'
    model = MoveAssistanceRequest
    success_url = reverse_lazy('moveassistancerequest_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(MoveAssistanceRequest, super().get_object()))
        return context


class MoveRequestViewListForConfirm(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_moverequest'
    model = MoveRequest
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(MoveRequest, self.request.user, 'orders', 'status', "date_of_creation",
                                                 "full_name"))
        context['title'] = "Список заявок для подтверждения"
        context['navigation'] = {context['title']: ""}
        return context

    def get_queryset(self):
        return MoveRequest.objects.filter(status="pen")


class MoveRequestViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_moverequest'
    model = MoveRequest
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(MoveRequest, self.request.user, 'orders', 'status', "date_of_creation",
                                                 "full_name"))
        return context


def context_for_view_move(user, transportForMove, employeeForMove):
    context = {'bool_perm_routs': get_bool_perm_for_user(user,
                                                         'orders', get_lower_name_cls(RouteMove)),
               'bool_perm_packings': get_bool_perm_for_user(user,
                                                            'orders', get_lower_name_cls(PackingForMove)),
               'bool_perm_transports': get_bool_perm_for_user(user,
                                                              'orders', get_lower_name_cls(transportForMove)),
               'bool_perm_employees': get_bool_perm_for_user(user,
                                                             'orders', get_lower_name_cls(employeeForMove)),
               'buttons_packings_urls': get_urls_for_interection(get_lower_name_cls(PackingForMove)),
               'buttons_routs_urls': get_urls_for_interection(get_lower_name_cls(RouteMove)),
               'buttons_transports_urls': get_urls_for_interection(get_lower_name_cls(transportForMove)),
               'buttons_employees_urls': get_urls_for_interection(get_lower_name_cls(employeeForMove))}
    return context


class MoveRequestView(LoginRequiredMixin, UserIsStaff,
                      PermissionRequiredMixin, generic.DetailView):
    permission_required = 'orders.view_moverequest'
    model = MoveRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = super().get_object()
        context.update(get_context_for_detail_view(MoveRequest, object, self.request.user, 'orders'))
        context['packings'] = PackingForMove.objects.filter(move_request=object)
        context['routs'] = RouteMove.objects.filter(move_request=object)
        context['transports'] = TransportForMoveRequest.objects.filter(move_request=object)
        context['employees'] = EmployeeForMoveRequest.objects.filter(move_request=object)
        context.update(context_for_view_move(self.request.user, TransportForMoveRequest, EmployeeForMoveRequest))
        return context


class MoveRequestCreate(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'orders.add_moverequest'
    model = MoveRequest
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(MoveRequest))
        return context


class MoveRequestChange(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'orders.change_moverequest'
    model = MoveRequest
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(MoveRequest, super().get_object()))
        return context


class MoveRequestDelete(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'orders.delete_moverequest'
    model = MoveRequest
    success_url = reverse_lazy('moverequest_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(MoveRequest, super().get_object()))
        return context


class MoveOrderViewListForExecution(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_moveorder'
    model = MoveOrder
    context_object_name = 'object_list'
    paginate_by = 10
    template_name = "orders/moveorder_executor_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            get_context_for_view_list(MoveOrder, self.request.user, 'orders'))
        context['title'] = "Список заказов для исполнителей"
        context['navigation'] = {context['title']: ""}
        return context

    def get_queryset(self):
        today = self.request.GET.get("today", False)
        with_me = self.request.GET.get("with_me", False)
        mos = MoveOrder.objects.filter(Q(move_request__status="con") | Q(move_request__status="ipr"))
        if today:
            mos = mos.filter(move_request__date_of_completion=datetime.datetime.today())

        return mos


class MoveOrderViewForExecution(LoginRequiredMixin, UserIsStaff,
                                PermissionRequiredMixin, generic.DetailView):
    permission_required = 'orders.view_moveorder'
    model = MoveOrder
    template_name = "orders/moveorder_executor_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = super().get_object()
        context.update(get_context_for_detail_view(MoveOrder, object, self.request.user, 'orders'))
        context['verbose'].update(get_verbose_of_fields_from_class(MoveRequest))
        context['packings'] = PackingForMove.objects.filter(move_request=object.move_request)
        context['routs'] = RouteMove.objects.filter(move_request=object.move_request)
        context['transports'] = TransportForMove.objects.filter(move_order=object)
        context['employees'] = EmployeeForMove.objects.filter(move_order=object)
        context.update(context_for_view_move(self.request.user, TransportForMove, EmployeeForMove))
        return context


class MoveOrderViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_moveorder'
    model = MoveOrder
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            get_context_for_view_list(MoveOrder, self.request.user, 'orders', 'move_request', "date_of_confirm",
                                      "total_cost"))
        return context


class MoveOrderView(LoginRequiredMixin, UserIsStaff,
                    PermissionRequiredMixin, generic.DetailView):
    permission_required = 'orders.view_moveorder'
    model = MoveOrder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = super().get_object()
        context.update(get_context_for_detail_view(MoveOrder, object, self.request.user, 'orders'))
        context['verbose'].update(get_verbose_of_fields_from_class(MoveRequest))
        context['packings'] = PackingForMove.objects.filter(move_request=object.move_request)
        context['routs'] = RouteMove.objects.filter(move_request=object.move_request)
        context['transports'] = TransportForMove.objects.filter(move_order=object)
        context['employees'] = EmployeeForMove.objects.filter(move_order=object)
        context.update(context_for_view_move(self.request.user, TransportForMove, EmployeeForMove))
        return context


class MoveOrderCreate(LoginRequiredMixin, UserIsStaff,
                      PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'orders.add_moveorder'
    model = MoveOrder
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(MoveOrder))
        return context


class MoveOrderChange(LoginRequiredMixin, UserIsStaff,
                      PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'orders.change_moveorder'
    model = MoveOrder
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(MoveOrder, super().get_object()))
        return context


class MoveOrderDelete(LoginRequiredMixin, UserIsStaff,
                      PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'orders.delete_moveorder'
    model = MoveOrder
    success_url = reverse_lazy('moveorder_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(MoveOrder, super().get_object()))
        return context


class EmployeeForMoveViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_employeeformove'
    model = EmployeeForMove
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(EmployeeForMove, self.request.user, 'orders', 'move_order',
                                                 "group", "employee", "hired_hours"))
        return context


class EmployeeForMoveView(LoginRequiredMixin, UserIsStaff,
                          PermissionRequiredMixin, generic.DetailView):
    permission_required = 'orders.view_employeeformove'
    model = EmployeeForMove

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(EmployeeForMove, super().get_object(), self.request.user, 'orders'))
        return context


class EmployeeForMoveCreate(LoginRequiredMixin, UserIsStaff,
                            PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'orders.add_employeeformove'
    model = EmployeeForMove
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(EmployeeForMove))
        return context


class EmployeeForMoveChange(LoginRequiredMixin, UserIsStaff,
                            PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'orders.change_employeeformove'
    model = EmployeeForMove
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(EmployeeForMove, super().get_object()))
        return context


class EmployeeForMoveDelete(LoginRequiredMixin, UserIsStaff,
                            PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'orders.delete_employeeformove'
    model = EmployeeForMove
    success_url = reverse_lazy('employeeformove_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(EmployeeForMove, super().get_object()))
        return context


class TransportForMoveViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_transportformove'
    model = TransportForMove
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(TransportForMove, self.request.user, 'orders', 'move_order',
                                                 "mode_transport", "transport", "hired_hours"))
        return context


class TransportForMoveView(LoginRequiredMixin, UserIsStaff,
                           PermissionRequiredMixin, generic.DetailView):
    permission_required = 'orders.view_transportformove'
    model = TransportForMove

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(TransportForMove, super().get_object(), self.request.user, 'orders'))
        return context


class TransportForMoveCreate(LoginRequiredMixin, UserIsStaff,
                             PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'orders.add_transportformove'
    model = TransportForMove
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(TransportForMove))
        return context


class TransportForMoveChange(LoginRequiredMixin, UserIsStaff,
                             PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'orders.change_transportformove'
    model = TransportForMove
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(TransportForMove, super().get_object()))
        return context


class TransportForMoveDelete(LoginRequiredMixin, UserIsStaff,
                             PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'orders.delete_transportformove'
    model = TransportForMove
    success_url = reverse_lazy('transportformove_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(TransportForMove, super().get_object()))
        return context


class PackingForMoveViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_packingformove'
    model = PackingForMove
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(PackingForMove, self.request.user, 'orders', 'move_request',
                                                 "packing", "total"))
        return context


class PackingForMoveView(LoginRequiredMixin, UserIsStaff,
                         PermissionRequiredMixin, generic.DetailView):
    permission_required = 'orders.view_packingformove'
    model = PackingForMove

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(PackingForMove, super().get_object(), self.request.user, 'orders'))
        return context


class PackingForMoveCreate(LoginRequiredMixin, UserIsStaff,
                           PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'orders.add_packingformove'
    model = PackingForMove
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(PackingForMove))
        return context


class PackingForMoveChange(LoginRequiredMixin, UserIsStaff,
                           PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'orders.change_packingformove'
    model = PackingForMove
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(PackingForMove, super().get_object()))
        return context


class PackingForMoveDelete(LoginRequiredMixin, UserIsStaff,
                           PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'orders.delete_packingformove'
    model = PackingForMove
    success_url = reverse_lazy('packingformove_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(PackingForMove, super().get_object()))
        return context


class RouteMoveViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_routemove'
    model = RouteMove
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(RouteMove, self.request.user, 'orders', 'move_request',
                                                 "point_a", "point_b", "distance"))
        return context


class RouteMoveView(LoginRequiredMixin, UserIsStaff,
                    PermissionRequiredMixin, generic.DetailView):
    permission_required = 'orders.view_routemove'
    model = RouteMove

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(RouteMove, super().get_object(), self.request.user, 'orders'))
        return context


class RouteMoveCreate(LoginRequiredMixin, UserIsStaff,
                      PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'orders.add_routemove'
    model = RouteMove
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(RouteMove))
        return context


class RouteMoveChange(LoginRequiredMixin, UserIsStaff,
                      PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'orders.change_routemove'
    model = RouteMove
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(RouteMove, super().get_object()))
        return context


class RouteMoveDelete(LoginRequiredMixin, UserIsStaff,
                      PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'orders.delete_routemove'
    model = RouteMove
    success_url = reverse_lazy('routemove_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(RouteMove, super().get_object()))
        return context


class EmployeeForMoveRequestViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_employeeformoverequest'
    model = EmployeeForMoveRequest
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(EmployeeForMoveRequest, self.request.user, 'orders', 'move_request',
                                                 "group", "total", "hired_hours"))
        return context


class EmployeeForMoveRequestView(LoginRequiredMixin, UserIsStaff,
                                 PermissionRequiredMixin, generic.DetailView):
    permission_required = 'orders.view_employeeformoverequest'
    model = EmployeeForMoveRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            get_context_for_detail_view(EmployeeForMoveRequest, super().get_object(), self.request.user, 'orders'))
        return context


class EmployeeForMoveRequestCreate(LoginRequiredMixin, UserIsStaff,
                                   PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'orders.add_employeeformoverequest'
    model = EmployeeForMoveRequest
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(EmployeeForMoveRequest))
        return context


class EmployeeForMoveRequestChange(LoginRequiredMixin, UserIsStaff,
                                   PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'orders.change_employeeformoverequest'
    model = EmployeeForMoveRequest
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(EmployeeForMoveRequest, super().get_object()))
        return context


class EmployeeForMoveRequestDelete(LoginRequiredMixin, UserIsStaff,
                                   PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'orders.delete_employeeformoverequest'
    model = EmployeeForMoveRequest
    success_url = reverse_lazy('employeeformoverequest_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(EmployeeForMoveRequest, super().get_object()))
        return context


class TransportForMoveRequestViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_transportformoverequest'
    model = TransportForMoveRequest
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(TransportForMoveRequest, self.request.user, 'orders', 'move_request',
                                                 "mode_transport", "total", "hired_hours"))
        return context


class TransportForMoveRequestView(LoginRequiredMixin, UserIsStaff,
                                  PermissionRequiredMixin, generic.DetailView):
    permission_required = 'orders.view_transportformoverequest'
    model = TransportForMoveRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            get_context_for_detail_view(TransportForMoveRequest, super().get_object(), self.request.user, 'orders'))
        return context


class TransportForMoveRequestCreate(LoginRequiredMixin, UserIsStaff,
                                    PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'orders.add_transportformoverequest'
    model = TransportForMoveRequest
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(TransportForMoveRequest))
        return context


class TransportForMoveRequestChange(LoginRequiredMixin, UserIsStaff,
                                    PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'orders.change_transportformoverequest'
    model = TransportForMoveRequest
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(TransportForMoveRequest, super().get_object()))
        return context


class TransportForMoveRequestDelete(LoginRequiredMixin, UserIsStaff,
                                    PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'orders.delete_transportformoverequest'
    model = TransportForMoveRequest
    success_url = reverse_lazy('transportformoverequest_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(TransportForMoveRequest, super().get_object()))
        return context
