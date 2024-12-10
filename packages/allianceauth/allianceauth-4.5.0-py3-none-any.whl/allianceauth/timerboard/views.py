import datetime
import logging

from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin,
)
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from allianceauth.eveonline.models import EveCorporationInfo
from allianceauth.timerboard.form import TimerForm
from allianceauth.timerboard.models import Timer

logger = logging.getLogger(__name__)

TIMER_VIEW_PERMISSION = 'auth.timer_view'
TIMER_MANAGE_PERMISSION = 'auth.timer_management'


class BaseTimerView(LoginRequiredMixin, PermissionRequiredMixin, View):
    pass


class TimerView(BaseTimerView):
    template_name = 'timerboard/view.html'
    permission_required = TIMER_VIEW_PERMISSION

    def get(self, request):
        logger.debug(f"timer_view called by user {request.user}")
        char = request.user.profile.main_character
        if char:
            corp = char.corporation
        else:
            corp = None
        base_query = Timer.objects.select_related('eve_character')
        render_items = {
            'timers': base_query.filter(corp_timer=False),
            'corp_timers': base_query.filter(corp_timer=True, eve_corp=corp),
            'future_timers': base_query.filter(corp_timer=False, eve_time__gte=timezone.now()),
            'past_timers': base_query.filter(corp_timer=False, eve_time__lt=timezone.now()),
        }

        return render(request, self.template_name, context=render_items)


class TimerManagementView(BaseTimerView):
    permission_required = TIMER_MANAGE_PERMISSION
    index_redirect = 'timerboard:view'
    success_url = reverse_lazy(index_redirect)
    model = Timer

    def get_timer(self, timer_id):
        return get_object_or_404(self.model, id=timer_id)


class AddUpdateMixin:
    def get_form_kwargs(self):
        """
        Inject the request user into the kwargs passed to the form
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class AddTimerView(TimerManagementView, AddUpdateMixin, CreateView):
    template_name_suffix = '_create_form'
    form_class = TimerForm

    def form_valid(self, form):
        result = super().form_valid(form)
        timer = self.object
        logger.info(
            f"Created new timer in {timer.system} at {timer.eve_time} by user {self.request.user}"
        )
        messages.success(
            self.request,
            _('Added new timer in %(system)s at %(time)s.') % {"system": timer.system, "time": timer.eve_time}
        )
        return result


class EditTimerView(TimerManagementView, AddUpdateMixin, UpdateView):
    template_name_suffix = '_update_form'
    form_class = TimerForm

    def form_valid(self, form):
        messages.success(self.request, _('Saved changes to the timer.'))
        return super().form_valid(form)


class RemoveTimerView(TimerManagementView, DeleteView):
    pass


def dashboard_timers(request):
    if request.user.has_perm(TIMER_VIEW_PERMISSION):
        try:
            corp = request.user.profile.main_character.corporation
        except (EveCorporationInfo.DoesNotExist, AttributeError):
            return ""

        timers = Timer.objects.select_related(
            'eve_character'
        ).filter(
            (Q(corp_timer=True) & Q(eve_corp=corp)) | Q(corp_timer=False),
            eve_time__gte=timezone.now()
        )[:5]

        if timers.count():
            context = {
                'timers': timers,
            }

            return render_to_string(
                template_name='timerboard/dashboard.timers.html',
                context=context, request=request
            )
        else:
            return ""
    else:
        return ""
