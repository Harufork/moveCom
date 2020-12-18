from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from .models import EmployeeRole, Profile, Employee, Notification
from additional_functions import get_context_for_view_list, get_context_for_detail_view, \
    get_context_for_form_view, get_context_for_delete_view, UserIsStaff
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User, Group


# class registration(View):
#     def get(self, request, *args, **kwargs):
#         context = {  }
#         return render(request, 'registration.html', context=context)
#     def post(self, request, *args, **kwargs):
#         username = request.POST['name']
#         password = request.POST['password']
#         if username and password:
#             if User.objects.filter(username=username).count() != 0:
#                 context = { 'info': 'Пользователь с таким именем уже есть в системе'}
#                 return render(request, 'registration.html', context=context)
#             else:
#                 User.objects.create_user(username=username, password=password)
#                 nUk = authenticate(username=username, password=password)
#                 login(request, nUk)
#                 return HttpResponseRedirect(reverse('main'))
#         else:
#             context = {'info': '!Не все поля заполнены!'}
#             return render(request, 'registration.html', context=context)

def registration(request):
    context = {
        'title': 'Регистрация'
    }
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            if User.objects.filter(username=phone_number).count() == 0:
                my_password = form.cleaned_data.get('password1')
                user = User.objects.create_user(username=phone_number, password=my_password)
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')
                user.save()

                user.profile.patronymic = form.cleaned_data.get('patronymic')
                user.profile.phone_number = form.cleaned_data.get('phone_number')
                user.profile.birth_date = form.cleaned_data.get('birth_date')
                user.profile.save()

                user = authenticate(username=user.username, password=form.cleaned_data.get('password1'))
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
        form = SignUpForm()
    context["form"] = form
    return render(request, 'registration/registration.html', context)


class NotifictionViewList(LoginRequiredMixin, UserIsStaff, generic.ListView):  # PermissionRequiredMixin
    # permission_required = 'orders.view_moveassistancerequest'
    model = Notification
    context_object_name = 'notification_list'

    # paginate_by = 10

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


# Create your views here.
class EmployeeRoleViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'users.view_employeerole'
    model = EmployeeRole
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(EmployeeRole, self.request.user, 'users', 'group', 'available'))
        return context


class EmployeeRoleView(LoginRequiredMixin, UserIsStaff,
                       PermissionRequiredMixin, generic.DetailView):
    permission_required = 'users.view_employeerole'
    model = EmployeeRole

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(EmployeeRole, super().get_object(), self.request.user, 'users'))
        return context


class EmployeeRoleCreate(LoginRequiredMixin, UserIsStaff,
                         PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'users.add_employeerole'
    model = EmployeeRole
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(EmployeeRole))
        return context


class EmployeeRoleChange(LoginRequiredMixin, UserIsStaff,
                         PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'users.change_employeerole'
    model = EmployeeRole
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(EmployeeRole, super().get_object()))
        return context


class EmployeeRoleDelete(LoginRequiredMixin, UserIsStaff,
                         PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'users.delete_employeerole'
    model = EmployeeRole
    success_url = reverse_lazy('users_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(EmployeeRole, super().get_object()))
        return context


# Create your views here.
class ProfileViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'users.view_profile'
    model = Profile
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(Profile, self.request.user, 'users', 'user'))
        return context


class ProfileView(LoginRequiredMixin, UserIsStaff,
                  PermissionRequiredMixin, generic.DetailView):
    permission_required = 'users.view_profile'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(Profile, super().get_object(), self.request.user, 'users'))
        return context


class ProfileCreate(LoginRequiredMixin, UserIsStaff,
                    PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'users.add_profile'
    model = Profile
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(Profile))
        return context


class ProfileChange(LoginRequiredMixin, UserIsStaff,
                    PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'users.change_profile'
    model = Profile
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(Profile, super().get_object()))
        return context


class ProfileDelete(LoginRequiredMixin, UserIsStaff,
                    PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'users.delete_profile'
    model = Profile
    success_url = reverse_lazy('users_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(Profile, super().get_object()))
        return context


# Create your views here.
class EmployeeViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'users.view_employee'
    model = Employee
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(Employee, self.request.user, 'users', 'user'))
        return context


class EmployeeView(LoginRequiredMixin, UserIsStaff,
                   PermissionRequiredMixin, generic.DetailView):
    permission_required = 'users.view_employee'
    model = Employee

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(Employee, super().get_object(), self.request.user, 'users'))
        return context


class EmployeeCreate(LoginRequiredMixin, UserIsStaff,
                     PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'users.add_employee'
    model = Employee
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(Employee))
        return context


class EmployeeChange(LoginRequiredMixin, UserIsStaff,
                     PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'users.change_employee'
    model = Employee
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(Employee, super().get_object()))
        return context


class EmployeeDelete(LoginRequiredMixin, UserIsStaff,
                     PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'users.delete_employee'
    model = Employee
    success_url = reverse_lazy('users_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(Employee, super().get_object()))
        return context

# Create your views here.
class GroupViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'auth.view_group'
    model = Group
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(Group, self.request.user, 'auth'))
        return context


class GroupView(LoginRequiredMixin, UserIsStaff,
                   PermissionRequiredMixin, generic.DetailView):
    permission_required = 'auth.view_group'
    model = Group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(Group, super().get_object(), self.request.user, 'auth'))
        return context


class GroupCreate(LoginRequiredMixin, UserIsStaff,
                     PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'auth.add_group'
    model = Group
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(Group))
        return context


class GroupChange(LoginRequiredMixin, UserIsStaff,
                     PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'auth.change_group'
    model = Group
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(Group, super().get_object()))
        return context


class GroupDelete(LoginRequiredMixin, UserIsStaff,
                     PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'auth.delete_group'
    model = Group
    success_url = reverse_lazy('users_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(Group, super().get_object()))
        return context

# Create your views here.
class UserViewList(LoginRequiredMixin, UserIsStaff, PermissionRequiredMixin, generic.ListView):
    permission_required = 'auth.view_user'
    model = User
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_view_list(User, self.request.user, 'auth'))
        return context


class UserView(LoginRequiredMixin, UserIsStaff,
                   PermissionRequiredMixin, generic.DetailView):
    permission_required = 'auth.view_user'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_detail_view(User, super().get_object(), self.request.user, 'auth'))
        return context


class UserCreate(LoginRequiredMixin, UserIsStaff,
                     PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = 'auth.add_user'
    model = User
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(User))
        return context


class UserChange(LoginRequiredMixin, UserIsStaff,
                     PermissionRequiredMixin, generic.edit.UpdateView):
    permission_required = 'auth.change_user'
    model = User
    fields = '__all__'
    template_name = "base_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_form_view(User, super().get_object()))
        return context


class UserDelete(LoginRequiredMixin, UserIsStaff,
                     PermissionRequiredMixin, generic.edit.DeleteView):
    permission_required = 'auth.delete_user'
    model = User
    success_url = reverse_lazy('users_list')
    context_object_name = 'object'
    template_name = "base_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_context_for_delete_view(User, super().get_object()))
        return context