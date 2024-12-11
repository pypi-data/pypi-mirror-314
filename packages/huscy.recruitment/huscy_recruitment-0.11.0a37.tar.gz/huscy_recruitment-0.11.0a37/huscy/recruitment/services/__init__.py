from django.db import models, transaction

from .attribute_filtersets import (
    apply_recruitment_criteria,
)
from huscy.recruitment.models import RecruitmentCriteria, SubjectGroup


__all__ = (
    'apply_recruitment_criteria',
    'create_subject_group',
    'delete_subject_group',
    'get_subject_groups',
    'update_subject_group',
)


@transaction.atomic
def create_subject_group(experiment, name, description=''):
    subject_group = SubjectGroup.objects.create(
        experiment=experiment,
        name=name,
        description=description,
        order=SubjectGroup.objects.filter(experiment=experiment).count(),
    )
    RecruitmentCriteria.objects.create(subject_group=subject_group)
    return subject_group


def delete_subject_group(subject_group):
    subject_groups_queryset = SubjectGroup.objects.filter(experiment=subject_group.experiment)

    if subject_groups_queryset.count() == 1:
        raise ValueError('Cannot delete subject group. At least one subject group must remain for '
                         'the experiment.')

    (subject_groups_queryset.filter(order__gt=subject_group.order)
                            .update(order=models.F('order') - 1))

    subject_group.delete()


def get_subject_groups(experiment):
    subject_groups_queryset = experiment.subject_groups.all()

    if not subject_groups_queryset.exists():
        create_subject_group(experiment, name='Subject group 1')

    return subject_groups_queryset


def update_recruitment_criteria(subject_group,
                                minimum_age_in_months=None,
                                maximum_age_in_months=None,
                                attribute_filterset={}):
    recruitment_criteria = subject_group.recruitment_criteria.latest('id')

    if recruitment_criteria.participation_requests.exists():
        recruitment_criteria = RecruitmentCriteria.objects.create(subject_group=subject_group)

    if minimum_age_in_months is not None:
        recruitment_criteria.minimum_age_in_months = minimum_age_in_months
    if maximum_age_in_months is not None:
        recruitment_criteria.maximum_age_in_months = maximum_age_in_months
    if attribute_filterset:
        recruitment_criteria.attribute_filterset = attribute_filterset

    recruitment_criteria.save()

    return subject_group


def update_subject_group(subject_group, name='', description=''):
    subject_group.name = name or subject_group.name
    subject_group.description = description or subject_group.description
    subject_group.save()
    return subject_group
