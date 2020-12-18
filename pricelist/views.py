from django.views import generic
from .models import PriceRole, PriceModeTDistance, PriceModeTransport, PricePacking
from additional_functions import get_context_for_view_list, get_context_for_detail_view,\
    get_context_for_form_view, get_context_for_delete_view, UserIsStaff
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy


class PriceRoleViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'pricelist.view_pricerole'
    model = PriceRole
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(PriceRole, self.request.user, 'pricelist', 'cost', 'creater',
                                                 'date_of_creation','effective_date','group'))
        return context


class PriceRoleView(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.DetailView):
    permission_required = 'pricelist.view_pricerole'
    model = PriceRole

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(PriceRole, super().get_object(), self.request.user, 'pricelist'))
        return context


class PriceRoleCreate(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'pricelist.add_pricerole'
    model = PriceRole
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(PriceRole))
        return context


class PriceRoleChange(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'pricelist.change_pricerole'
    model = PriceRole
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(PriceRole, super().get_object()))
        return context


class PriceRoleDelete(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'pricelist.delete_pricerole'
    model = PriceRole
    success_url = reverse_lazy('pricerole_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(PriceRole, super().get_object()))
        return context


class PriceModeTransportViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'pricelist.view_pricemodetransport'
    model = PriceModeTransport
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(PriceModeTransport, self.request.user, 'pricelist', 'cost', 'creater',
                                                 'date_of_creation','effective_date','mode_transport'))
        return context


class PriceModeTransportView(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.DetailView):
    permission_required = 'pricelist.view_pricemodetransport'
    model = PriceModeTransport

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(PriceModeTransport, super().get_object(), self.request.user, 'pricelist'))
        return context


class PriceModeTransportCreate(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'pricelist.add_pricemodetransport'
    model = PriceModeTransport
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(PriceModeTransport))
        return context


class PriceModeTransportChange(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'pricelist.change_pricemodetransport'
    model = PriceModeTransport
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(PriceModeTransport, super().get_object()))
        return context


class PriceModeTransportDelete(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'pricelist.delete_pricemodetransport'
    model = PriceModeTransport
    success_url = reverse_lazy('pricemodetransport_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(PriceModeTransport, super().get_object()))
        return context


class PriceModeTDistanceViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'pricelist.view_pricemodetdistance'
    model = PriceModeTDistance
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(PriceModeTDistance, self.request.user, 'pricelist', 'cost', 'creater',
                                                 'date_of_creation','effective_date','mode_transport'))
        return context


class PriceModeTDistanceView(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.DetailView):
    permission_required = 'pricelist.view_pricemodetdistance'
    model = PriceModeTDistance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(PriceModeTDistance, super().get_object(), self.request.user, 'pricelist'))
        return context


class PriceModeTDistanceCreate(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'pricelist.add_pricemodetdistance'
    model = PriceModeTDistance
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(PriceModeTDistance))
        return context


class PriceModeTDistanceChange(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'pricelist.change_pricemodetdistance'
    model = PriceModeTDistance
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(PriceModeTDistance, super().get_object()))
        return context


class PriceModeTDistanceDelete(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'pricelist.delete_pricemodetdistance'
    model = PriceModeTDistance
    success_url = reverse_lazy('pricemodetdistance_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(PriceModeTDistance, super().get_object()))
        return context



class PricePackingViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'pricelist.view_pricepacking'
    model = PricePacking
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(PricePacking, self.request.user, 'pricelist', 'cost', 'creater',
                                                 'date_of_creation','effective_date','packing'))
        return context


class PricePackingView(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.DetailView):
    permission_required = 'pricelist.view_pricepacking'
    model = PricePacking

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(PricePacking, super().get_object(), self.request.user, 'pricelist'))
        return context


class PricePackingCreate(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'pricelist.add_pricepacking'
    model = PricePacking
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(PricePacking))
        return context


class PricePackingChange(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'pricelist.change_pricepacking'
    model = PricePacking
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(PricePacking, super().get_object()))
        return context


class PricePackingDelete(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'pricelist.delete_pricepacking'
    model = PricePacking
    success_url = reverse_lazy('pricepacking_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(PricePacking, super().get_object()))
        return context