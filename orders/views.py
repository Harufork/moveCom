from django.shortcuts import render, get_object_or_404
from .forms import ForClientMoveRequest
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from .models import MoveAssistanceRequest, MoveRequest, MoveOrder,\
    EmployeeForMove, TransportForMove, PackingForMove, RouteMove
from additional_functions import get_context_for_view_list, get_context_for_detail_view,\
    get_context_for_form_view, get_context_for_delete_view, UserIsStaff
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from transport.models import ModeTransport
from packing.models import TypePacking, Packing
from users.models import EmployeeRole

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
                        quanity_nothing+=1
                    else:
                        context[name_id][key[2]].update({key[1]: value})
                        quanity_nothing-=1
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
                for i in range(value['quan']):
                    newEFM = EmployeeForMove()
                    newEFM.move_request = newMR
                    newEFM.group = EmployeeRole.objects.get(pk=key).group
                    newEFM.hired_hours = value['hird']
                    newEFM.save()

            for key, value in context["mode_transport_post"].items():
                for i in range(value['quan']):
                    newTFM = TransportForMove()
                    newTFM.move_request = newMR
                    newTFM.mode_transport = ModeTransport.objects.get(pk=key)
                    newTFM.rental_hours = value['hird']
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
    context['type_packings_with_packings'].update({additional_packing_name: Packing.objects.filter(available=True, type=None)})
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



# Create your views here.
class MoveAssistanceRequestViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_moveassistancerequest'
    model = MoveAssistanceRequest
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(MoveAssistanceRequest, self.request.user, 'orders', 'status', "date_of_creation", "full_name"))
        return context


class MoveAssistanceRequestView(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.DetailView):
    permission_required = 'orders.view_moveassistancerequest'
    model = MoveAssistanceRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(MoveAssistanceRequest, super().get_object(), self.request.user, 'orders'))
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

class MoveRequestViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_moverequest'
    model = MoveRequest
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(MoveRequest, self.request.user, 'orders', 'status', "date_of_creation", "full_name"))
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
        context['transports'] = TransportForMove.objects.filter(move_request=object)
        context['employees'] = EmployeeForMove.objects.filter(move_request=object)
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

class MoveOrderViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_moveorder'
    model = MoveOrder
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(MoveOrder, self.request.user, 'orders', 'move_request', "date_of_confirm", "total_cost"))
        return context


class MoveOrderView(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.DetailView):
    permission_required = 'orders.view_moveorder'
    model = MoveOrder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(MoveOrder, super().get_object(), self.request.user, 'orders'))
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