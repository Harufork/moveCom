from django.views import generic
from .models import Transport, ModeTransport
from additional_functions import get_context_for_view_list, get_context_for_detail_view,\
    get_context_for_form_view, get_context_for_delete_view, UserIsStaff
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy


# Create your views here.
class TransportViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'transport.view_transport'
    model = Transport
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(Transport, self.request.user, 'transport', 'name', 'mode'))
        return context


class TransportView(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.DetailView):
    permission_required = 'transport.view_transport'
    model = Transport

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(Transport, super().get_object(), self.request.user, 'transport'))
        return context


class TransportCreate(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'transport.add_transport'
    model = Transport
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(Transport))
        return context


class TransportChange(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'transport.change_transport'
    model = Transport
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(Transport, super().get_object()))
        return context


class TransportDelete(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'transport.delete_transport'
    model = Transport
    success_url = reverse_lazy('transport_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(Transport, super().get_object()))
        return context

# Create your views here.
class ModeTransportViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'transport.view_modetransport'
    model = ModeTransport
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(ModeTransport, self.request.user, 'transport', 'name'))
        return context


class ModeTransportView(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.DetailView):
    permission_required = 'transport.view_modetransport'
    model = ModeTransport

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(ModeTransport, super().get_object(), self.request.user, 'transport'))
        return context


class ModeTransportCreate(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'transport.add_modetransport'
    model = ModeTransport
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(ModeTransport))
        return context


class ModeTransportChange(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'transport.change_modetransport'
    model = ModeTransport
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(Transport, super().get_object()))
        return context


class ModeTransportDelete(LoginRequiredMixin, UserIsStaff,
                        PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'transport.delete_modetransport'
    model = ModeTransport
    success_url = reverse_lazy('transport_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(ModeTransport, super().get_object()))
        return context
