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
    fields = None

    form = None

    msg_name_class = None

    msg_add_name = None
    msg_add_success = _('%(class)s <strong>%(name)s</strong> added successfully')
    msg_add_not_valid = _('Cannot add %(class)s <strong>%(name)s</strong>, the form contains errors')
    msg_add_integrity_error = _('Cannot add %(class)s <strong>%(name)s</strong>, it contains logic error(s)')

    msg_edit_name = None
    msg_edit_success = _('%(class)s <strong>%(name)s</strong> updated successfully')
    msg_edit_not_changed = _('%(class)s <strong>%(name)s</strong> was not changed')
    msg_edit_not_valid = _('Cannot update %(class)s <strong>%(name)s</strong>, the form contains errors')
    msg_edit_integrity_error = _('Cannot update %(class)s <strong>%(name)s</strong>, it contains logic error(s)')

    def get(self, request):
        request_id = request.GET.get(self.object_id_key)
        object_instance = get_object_or_404(self.model, id=request_id, User=request.user)
        # TODO: Maybe it's better to create and serialize a CounterpartyForm here?
        object_dict = model_to_dict(object_instance, fields=self.fields)
        return JsonResponse(object_dict)

    def post(self, request):
        action = request.POST.get(self.action_key)
        if action == 'add':
            object_form = self.form(request.POST)
            if not object_form.is_valid():
                msg = self.msg_add_not_valid % {'class': self.msg_name_class, 'name': self.msg_add_name}
                return JsonResponse({'status': 'not_valid',
                                     'message': {'text': msg, 'level': 'Error'},
                                     'errors': object_form.errors})
            object_instance = object_form.save(commit=False)
            object_instance.User = request.user
            try:
                object_instance.save()
                messages.success(request,
                                 self.msg_add_success % {'class': self.msg_name_class, 'name': self.msg_add_name})
                return JsonResponse({'status': 'success'})  # 'success' causes CRUD logic to refresh the page
            except IntegrityError as e:
                msg = self.msg_add_integrity_error % {'class': self.msg_name_class, 'name': self.msg_add_name}
                return JsonResponse({'status': 'not_valid',
                                     'message': {'text': msg, 'level': 'Error'},
                                     'errors': e.args})
        elif action == 'edit':
            request_id = request.POST.get(self.object_id_key)
            object_instance = get_object_or_404(self.model, id=request_id, User=request.user)
            object_form = self.form(request.POST, instance=object_instance)
            if not object_form.has_changed():
                msg = self.msg_edit_not_changed % {'class': self.msg_name_class, 'name': self.msg_add_name}
                return JsonResponse({'status': 'not_changed',
                                     'message': {'text': msg, 'level': 'Warning'}})
            if not object_form.is_valid():
                msg = self.msg_edit_not_valid % {'class': self.msg_name_class, 'name': self.msg_add_name}
                return JsonResponse({'status': 'not_valid',
                                     'message': {'text': msg, 'level': 'Error'},
                                     'errors': object_form.errors})
            try:
                object_form.save()
                messages.success(request,
                                 self.msg_edit_success % {'class': self.msg_name_class, 'name': self.msg_add_name})
                return JsonResponse({'status': 'success'})  # 'success' causes CRUD logic to refresh the page
            except IntegrityError as e:
                msg = self.msg_edit_integrity_error % {'class': self.msg_name_class, 'name': self.msg_add_name}
                # messages.error(request, msg)
                return JsonResponse({'status': 'not_valid',
                                     'message': {'text': msg, 'level': 'Error'},
                                     'errors': e.args})
        else:
            return HttpResponseBadRequest()
