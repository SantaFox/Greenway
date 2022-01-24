from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View


@method_decorator(login_required, name='dispatch')
class CrudActionView(View):
    http_method_names = ['get', 'post']

    object_id_key = 'id'
    action_key = 'action'

    model = None
    user_id_field = 'User'
    fields = None
    exclude = {'User'}
    form = None

    parent_id_key = 'parent_id'
    parent_id_field = None
    parent_user_id_field = 'User'
    parent_model = None

    msg_name_class = None

    msg_add_name = None         # item_form.cleaned_data["Name"]
    msg_add_success = _('%(class)s <strong>%(name)s</strong> added successfully')
    msg_add_not_valid = _('Cannot add %(class)s <strong>%(name)s</strong>, the form contains errors')
    msg_add_integrity_error = _('Cannot add %(class)s <strong>%(name)s</strong>, it contains logic error(s)')

    msg_edit_name = lambda self, instance: instance.__str__()
    msg_edit_success = _('%(class)s <strong>%(name)s</strong> updated successfully')
    msg_edit_not_changed = _('%(class)s <strong>%(name)s</strong> was not changed')
    msg_edit_not_valid = _('Cannot update %(class)s <strong>%(name)s</strong>, the form contains errors')
    msg_edit_integrity_error = _('Cannot update %(class)s <strong>%(name)s</strong>, it contains logic error(s)')

    def get(self, request):
        request_id = request.GET.get(self.object_id_key)
        parent_id = request.GET.get(self.parent_id_key)

        user_filter = {self.user_id_field: request.user}
        parent_user_filter = {self.parent_user_id_field: request.user}

        if request_id:
            # edit existing object
            object_instance = get_object_or_404(self.model, id=request_id, **user_filter)
            object_form = self.form(instance=object_instance)
        else:
            # add new - need some initial data. However, the instance itself may not contain a User field if
            # the parent instance have; so we need to check. However, I have no idea why User may be needed,
            # because it will be anyway excluded later.
            object_instance = self.model()
            if self.user_id_field in [f.name for f in object_instance._meta.get_fields()]:
                setattr(object_instance, self.user_id_field, request.user)
            if parent_id:
                parent_instance = get_object_or_404(self.parent_model, id=parent_id, **parent_user_filter)
                setattr(object_instance, self.parent_id_field, parent_instance)
            params = self.get_default_info(object_instance)
            for attr, value in params.items():
                setattr(object_instance, attr, value)
            object_form = self.form(initial=params)

        # TODO: Maybe it's better to create and serialize a CounterpartyForm here?

        object_dict = model_to_dict(object_instance, fields=self.fields, exclude=self.exclude)
        object_dict_add = self.get_additional_info(object_instance)
        tech_dict = {}
        if request_id: tech_dict[self.object_id_key] = request_id
        if parent_id: tech_dict[self.parent_id_key] = parent_id
        return JsonResponse({**object_dict, **object_dict_add, **tech_dict})

    def post(self, request):
        request_id = request.POST.get(self.object_id_key)
        parent_id = request.POST.get(self.parent_id_key)

        user_filter = {self.user_id_field: request.user}
        parent_user_filter = {self.parent_user_id_field: request.user}

        action = request.POST.get(self.action_key)

        if action == 'add':
            object_form = self.form(request.POST)
            if not object_form.is_valid():
                msg = self.msg_add_not_valid % {'class': self.msg_name_class, 'name': self.msg_add_name}
                return JsonResponse({'status': 'not_valid',
                                     'message': {'text': msg, 'level': 'Error'},
                                     'errors': object_form.errors})
            object_instance = object_form.save(commit=False)
            if self.user_id_field in [f.name for f in object_instance._meta.get_fields()]:
                setattr(object_instance, self.user_id_field, request.user)
            if parent_id:
                parent_instance = get_object_or_404(self.parent_model, id=parent_id, **parent_user_filter)
                setattr(object_instance, self.parent_id_field, parent_instance)
            try:
                object_instance.save()
                messages.success(request,
                                 self.msg_add_success % {'class': self.msg_name_class, 'name': self.msg_edit_name(object_instance)})
                return JsonResponse({'status': 'success'})  # 'success' causes CRUD logic to refresh the page
            except IntegrityError as e:
                msg = self.msg_add_integrity_error % {'class': self.msg_name_class, 'name': self.msg_edit_name(object_instance)}
                return JsonResponse({'status': 'not_valid',
                                     'message': {'text': msg, 'level': 'Error'},
                                     'errors': e.args})
        elif action == 'edit':
            object_instance = get_object_or_404(self.model, id=request_id, **user_filter)
            object_form = self.form(request.POST, instance=object_instance)
            if not object_form.has_changed():
                msg = self.msg_edit_not_changed % {'class': self.msg_name_class, 'name': self.msg_edit_name(object_instance)}
                return JsonResponse({'status': 'not_changed',
                                     'message': {'text': msg, 'level': 'Warning'}})
            if not object_form.is_valid():
                msg = self.msg_edit_not_valid % {'class': self.msg_name_class, 'name': self.msg_edit_name(object_instance)}
                return JsonResponse({'status': 'not_valid',
                                     'message': {'text': msg, 'level': 'Error'},
                                     'errors': object_form.errors})
            try:
                object_form.save()
                messages.success(request,
                                 self.msg_edit_success % {'class': self.msg_name_class, 'name': self.msg_edit_name(object_instance)})
                return JsonResponse({'status': 'success'})  # 'success' causes CRUD logic to refresh the page
            except IntegrityError as e:
                msg = self.msg_edit_integrity_error % {'class': self.msg_name_class, 'name': self.msg_edit_name(object_instance)}
                # messages.error(request, msg)
                return JsonResponse({'status': 'not_valid',
                                     'message': {'text': msg, 'level': 'Error'},
                                     'errors': e.args})
        else:
            return HttpResponseBadRequest()

    def get_default_info(self, instance):
        return dict()

    def get_additional_info(self, instance):
        return dict()


@method_decorator(login_required, name='dispatch')
class CrudDeleteView(View):
    http_method_names = ['get', 'post']

    object_id_key = 'id'

    model = None

    msg_name_class = None

    msg_name = None        #
    msg_success = _('%(class)s <strong>%(name)s</strong> deleted successfully')
    msg_not_exist = _('Cannot delete %(class)s <strong>%(name)s</strong> as it doesn"t exists')
    msg_integrity_error = _('Cannot delete %(class)s <strong>%(name)s</strong>, it contains logic error(s)')

    def get(self, request):
        request_id = request.GET.get(self.object_id_key)
        try:
            object_instance = self.model.objects.get(id=request_id, User=request.user)
        except self.model.DoesNotExist as e:
            msg = self.msg_not_exist % {'class': self.msg_name_class, 'name': self.msg_name}
            # messages.error(request, msg)
            return JsonResponse({'status': 'not_exist',
                                 'message': {'text': msg, 'level': 'Error'},
                                 'errors': e.args})

        related = object_instance.is_deletable()
        if related:
            related_dict = {str(rel.model._meta.verbose_name_plural): list(i.__str__() for i in rel.all()) for rel in
                            related}
            return JsonResponse({'status': 'related_found',
                                 'related': related_dict})
        else:
            return JsonResponse({'status': 'ok'})

    def post(self, request):
        request_id = request.POST.get(self.object_id_key)
        try:
            object_instance = self.model.objects.get(id=request_id, User=request.user)
        except self.model.DoesNotExist as e:
            msg = self.msg_not_exist % {'class': self.msg_name_class, 'name': self.msg_name}
            # messages.error(request, msg)
            return JsonResponse({'status': 'not_exist',
                                 'message': {'text': msg, 'level': 'Error'},
                                 'errors': e.args})
        try:
            object_instance.delete()
            messages.success(request,
                             self.msg_success % {'class': self.msg_name_class, 'name': self.msg_name})
            return JsonResponse({'status': 'success'})
        except IntegrityError as e:
            msg = self.msg_integrity_error % {'class': self.msg_name_class, 'name': self.msg_name}
            # messages.error(request, msg)
            return JsonResponse({'status': 'not_valid',
                                 'message': {'text': msg, 'level': 'Error'},
                                 'errors': e.args})