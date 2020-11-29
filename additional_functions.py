from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin

class UserIsStaff(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


def get_verbose_of_fields_from_class_with_param(cls, *args):
    """Возвращает значения подробного названия выбранных полей класса,
    на основе введённых полей в args"""
    return { "verbose" : {name: cls._meta.get_field(name).verbose_name for name in args} }

def get_verbose_of_field_from_class(cls, field):
    """Возвращает значения подробного названия выбранного поля класса"""
    return cls._meta.get_field(field).verbose_name

def get_verbose_of_fields_from_class(cls):
    """Возвращает значения подробного названия выбранных полей класса"""
    return { "verbose" : {fn.name: fn.verbose_name  for fn in cls._meta.get_fields() if hasattr(fn, 'verbose_name')} }


def get_cls_verbose_name_plural(cls):
    """Возвращает подробное название класа во множественном числе"""
    return cls._meta.verbose_name_plural


def get_cls_verbose_name(cls):
    """Возвращает подробное название класаа"""
    return cls._meta.verbose_name


def get_bool_perm_for_user(user, app_name, cls_name):
    return {
        'view': user.has_perm(app_name + ".view_" + cls_name),
        'add': user.has_perm(app_name + ".add_" + cls_name),
        'change': user.has_perm(app_name + ".change_" + cls_name),
        'delete': user.has_perm(app_name + ".delete_" + cls_name),
    }


def get_urls_for_interection(cls_name):
    return {
        'add': reverse("add_" + cls_name),
        'abstract_change': "change_" + cls_name,
        'abstract_delete': "delete_" + cls_name,
    }


def get_urls_of_object_for_interaction(cls_name, pk):
    return {
        # 'add': reverse("add_" + cls_name),
        'change': reverse("change_" + cls_name, args=[pk]),
        'delete': reverse("delete_" + cls_name, args=[pk]),
    }


def get_context_for_view_list(cls, user, app_name, *args):
    context = get_verbose_of_fields_from_class_with_param(cls, *args)
    context['title'] = get_cls_verbose_name_plural(cls)
    cls_name = cls.__name__.lower()
    context['navigation'] = {context['title']: ""}
    context['buttons_urls'] = get_urls_for_interection(cls_name)
    context["bool_perm_of_user"] = get_bool_perm_for_user(user, app_name, cls_name)
    return context


def get_context_for_detail_view(cls, object, user, app_name):
    context = get_verbose_of_fields_from_class(cls)
    context['title'] = f"{get_cls_verbose_name(cls)}: {object}"
    cls_name = cls.__name__.lower()
    context["bool_perm_of_user"] = get_bool_perm_for_user(user, app_name, cls_name)
    context['buttons_urls'] = get_urls_of_object_for_interaction(cls_name, object.pk)
    context['navigation'] = {
        get_cls_verbose_name_plural(cls): reverse(cls_name + "_list"),
        context['title']: ""
    }
    return context


def get_context_for_form_view(cls, object=None):
    context = {'title': f"Cоздать {get_cls_verbose_name(cls).lower()}" if object == None \
        else f"Редактировать {get_cls_verbose_name(cls).lower()}: {object}"}
    context['navigation'] = {
        get_cls_verbose_name_plural(cls): reverse(cls.__name__.lower() + "_list"),
        context['title']: ""
    }
    context['text_button'] = "Создать" if object == None else "Сохрнить изменения"
    return context


def get_context_for_delete_view(cls, object):
    context = {'title': f"Удалить {get_cls_verbose_name(cls).lower()}: {object}"}
    context['navigation'] = {
        get_cls_verbose_name_plural(cls): reverse(cls.__name__.lower() + "_list"),
        context['title']: ""
    }
    return context

def isInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

