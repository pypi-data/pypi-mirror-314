from enum import Enum

from django.conf import settings
from django.db import models

from django.utils.translation import gettext_lazy as _

# from huscy.appointments.models import Appointment
from huscy.project_design.models import Experiment


def _get_setting(key, default):
    huscy_settings = getattr(settings, 'HUSCY', {})
    recruitment_settings = huscy_settings.get('recruitment', {})
    return recruitment_settings.get(key, default)


DEFAULT_AGE_RANGE = _get_setting('default_age_range', (18, 40))


class SubjectGroup(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE,
                                   related_name='subject_groups')
    name = models.CharField(max_length=126)
    description = models.TextField(blank=True, default='')
    order = models.PositiveSmallIntegerField(blank=True, default=0)


class RecruitmentCriteria(models.Model):
    subject_group = models.ForeignKey(SubjectGroup, on_delete=models.CASCADE,
                                      related_name='recruitment_criteria')

    minimum_age_in_months = models.PositiveSmallIntegerField(default=DEFAULT_AGE_RANGE[0])
    maximum_age_in_months = models.PositiveSmallIntegerField(default=DEFAULT_AGE_RANGE[1])

    attribute_filterset = models.JSONField(default=dict)


class ParticipationRequest(models.Model):
    class STATUS(Enum):
        pending = (0, _('Pending'))
        invited = (1, _('Invited'))

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    recruitment_criteria = models.ForeignKey(RecruitmentCriteria, on_delete=models.PROTECT,
                                             related_name='participation_requests')

    pseudonym = models.CharField(max_length=255, verbose_name=_('Pseudonym'), unique=True)
    status = models.PositiveSmallIntegerField(choices=[x.value for x in STATUS],
                                              default=STATUS.get_value('pending'),
                                              verbose_name=_('Status'))

    created_at = models.DateTimeField(auto_now_add=True)


"""
class Recall(models.Model):
    participation_request = models.ForeignKey(ParticipationRequest, on_delete=models.CASCADE,
                                              related_name='recall')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
"""
