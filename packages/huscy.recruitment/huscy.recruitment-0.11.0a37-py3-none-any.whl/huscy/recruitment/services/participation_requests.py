"""
from datetime import timedelta

from django.contrib.contenttypes.models import ContentType

from huscy.appointments.services import create_appointment
from huscy.pseudonyms.models import Pseudonym
from huscy.pseudonyms.services import get_or_create_pseudonym
from huscy.recruitment.models import ParticipationRequest, Recall


def get_participation_requests_for_experiment(experiment):
    return (ParticipationRequest.objects
                                .filter(attribute_filterset__subject_group__experiment=experiment))


def create_or_update_participation_request(subject, attribute_filterset, status, **kwargs):
    content_type = ContentType.objects.get_by_natural_key('recruitment', 'participationrequest')
    pseudonym = get_or_create_pseudonym(
        subject=subject,
        content_type=content_type,
        object_id=attribute_filterset.subject_group.experiment_id
    )

    participation_request, created = ParticipationRequest.objects.get_or_create(
        pseudonym=pseudonym.code,
        attribute_filterset=attribute_filterset,
        defaults=dict(status=status),
    )

    if not created and not participation_request.status == status:
        participation_request.status = status
        participation_request.save(update_fields=['status'])

    if status == ParticipationRequest.STATUS.get_value('pending') and 'appointment' in kwargs:
        creator = kwargs['user']
        start = kwargs['appointment']
        end = start + timedelta(minutes=30)

        try:
            recall = participation_request.recall.get()
            # TODO: create new appointment, if appointment.start is in the past
            recall.appointment.creator = creator
            recall.appointment.start = start
            recall.appointment.end = end
            recall.appointment.save()
        except Recall.DoesNotExist:
            appointment = create_appointment(creator=creator, start=start, end=end,
                                             title='recall appointment')
            Recall.objects.create(participation_request=participation_request,
                                  appointment=appointment)

    return participation_request


def get_participation_requests(subject=None, attribute_filterset=None):
    if attribute_filterset is None and subject is None:
        raise ValueError('Expected either attribute_filterset or subject args')

    pseudonyms = []
    if subject:
        content_type = ContentType.objects.get_by_natural_key('recruitment', 'participationrequest')
        pseudonyms = (Pseudonym.objects.filter(subject=subject, content_type=content_type)
                                       .values_list('code', flat=True))
    if attribute_filterset and subject:
        return ParticipationRequest.objects.filter(pseudonym__in=pseudonyms,
                                                   attribute_filterset=attribute_filterset)
    elif attribute_filterset:
        return ParticipationRequest.objects.filter(attribute_filterset=attribute_filterset)
    return ParticipationRequest.objects.filter(pseudonym__in=pseudonyms)
"""
