from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from .models import TypePacking, Measurement, Packing
from additional_functions import get_context_for_view_list, get_context_for_detail_view,\
    get_context_for_form_view, get_context_for_delete_view, UserIsStaff
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from . import forms
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy


# class TypeRenw(View):
#     def get(self, request, pk, *args, **kwargs):
#         type = get_object_or_404(TypePacking, pk=pk)
#         context = {'form': forms.EditTypePacking(initial={'name': type.name}) }
#         return render(request, 'packing/renwtype.html', context=context)
#     def post(self, request, pk, *args, **kwargs):
#         type = get_object_or_404(TypePacking, pk=pk)
#         form = forms.EditTypePacking(request.POST)
#         if form.is_valid():
#             type.name = form.cleaned_data['name']
#             type.save()
#             return HttpResponseRedirect(reverse('type_packing',args=[pk]))
#         return render(request, 'packing/renwtype.html', context={'title':"ошибка", 'form':form})


class TypePackingViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'packing.view_typepacking'
    model = TypePacking # Модель, на основе которой будет создаваться список
    context_object_name = 'object_list'
    paginate_by = 10
    # context_object_name = 'type_packing_list'  # ваше собственное имя переменной контекста в шаблоне
    # // поумолчанию имямодели_list
    # queryset = TypePacking.objects.filter(name__icontains='в')[:5]  # Фильтр, то какие объекты нужно вывести
    # template_name = "typepackinglist.html" # Расположение хтмл файла
    # // именно здесь, что на 1 уровне темлпатес
    # // имя формируется из имямодели_list.html
    # def get_queryset(self):
    #     return TypePacking.objects.filter(name__icontains='в')[:5]  # То же самое, что выше, но как метод

    def get_context_data(self, **kwargs):  # Для формирование контекста
        context = super().get_context_data(**kwargs)

        # Получение контекста, который сформировал generic.ListView
        context.update(get_context_for_view_list(TypePacking, self.request.user, 'packing', 'name'))
        return context


class TypePackingView(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.DetailView):
    permission_required = 'packing.view_typepacking'
    model = TypePacking

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(TypePacking, super().get_object(), self.request.user, 'packing'))
        return context


class TypePackingCreate(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'packing.add_typepacking'
    model = TypePacking
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(TypePacking))
        return context


class TypePackingChange(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'packing.change_typepacking'
    model = TypePacking
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(TypePacking, super().get_object()))
        return context


class TypePackingDelete(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'packing.delete_typepacking'
    model = TypePacking
    success_url = reverse_lazy('typepacking_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(TypePacking, super().get_object()))
        return context


class MeasurementViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'packing.view_measurement'
    model = Measurement
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(Measurement, self.request.user, 'packing', 'name', "symbol"))
        return context


class MeasurementView(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.DetailView):
    permission_required = 'packing.view_measurement'
    model = Measurement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(Measurement, super().get_object(), self.request.user, 'packing'))
        return context


class MeasurementCreate(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'packing.add_measurement'
    model = Measurement
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(Measurement))
        return context


class MeasurementChange(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'packing.change_measurement'
    model = Measurement
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(Measurement, super().get_object()))
        return context


class MeasurementDelete(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'packing.delete_measurement'
    model = Measurement
    success_url = reverse_lazy('measurement_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(Measurement, super().get_object()))
        return context


class PackingViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'packing.view_packing'
    model = Packing
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(Packing, self.request.user, 'packing', 'name', 'available',  'type', 'unit'))
        return context


class PackingView(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.DetailView):
    permission_required = 'packing.view_packing'
    model = Packing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(Packing, super().get_object(), self.request.user, 'packing'))
        return context


class PackingCreate(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'packing.add_packing'
    model = Packing
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(Packing))
        return context


class PackingChange(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'packing.change_packing'
    model = Packing
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(Packing, super().get_object()))
        return context


class PackingDelete(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'packing.delete_packing'
    model = Packing
    success_url = reverse_lazy('packing_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(Packing, super().get_object()))
        return context

