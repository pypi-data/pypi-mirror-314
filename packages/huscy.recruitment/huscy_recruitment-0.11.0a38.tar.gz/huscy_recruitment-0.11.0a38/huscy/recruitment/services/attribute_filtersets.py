import operator
from functools import reduce

from django.db.models import Q

from huscy.attributes.models import AttributeSet
from huscy.attributes.services import get_attribute_schema
from huscy.pseudonyms.services import get_subjects as get_subjects_by_pseudonym
from huscy.recruitment.models import ParticipationRequest
from huscy.subjects.services import get_subjects


def apply_recruitment_criteria(recruitment_criteria, include_children=False):
    attribute_sets = _filter_attributesets_by_filterset(recruitment_criteria)
    matching_subjects = get_subjects_by_pseudonym([attribute_set.pseudonym
                                                   for attribute_set in attribute_sets])

    matching_subjects = (matching_subjects.select_related('contact')
                                          .prefetch_related('legal_representatives')
                                          .order_by('contact__last_name', 'contact__first_name'))
    not_invited_matching_subjects = _exclude_invited_subjects(matching_subjects,
                                                              recruitment_criteria)

    return not_invited_matching_subjects.intersection(get_subjects(include_children))


def _filter_attributesets_by_filterset(recruitment_criteria):
    filters = _get_filters(recruitment_criteria.attribute_filterset)
    return AttributeSet.objects.filter(*filters)


def _get_filters(attribute_filterset):
    attribute_schema = get_attribute_schema()

    for attribute_name, filter_values in attribute_filterset.items():
        exclude = False

        if attribute_name.startswith('-'):
            attribute_name = attribute_name[1:]
            exclude = True

        attribute_type = _get_attribute_type(attribute_schema.schema, attribute_name)

        if attribute_type in ['integer', 'number']:
            lookup = f'attributes__{attribute_name}__range'
        elif attribute_type == 'array':
            lookup = f'attributes__{attribute_name}__contains'
        else:
            lookup = f'attributes__{attribute_name}'

        q = reduce(operator.or_, (Q(**{lookup: filter_value}) for filter_value in filter_values))

        if exclude:
            q = ~Q(q)

        yield q


def _get_attribute_type(schema, attribute_name):
    path = ['properties'] + attribute_name.replace('__', '__properties__').split('__')
    attribute = reduce(operator.getitem, path, schema)
    return attribute['type']


def _exclude_invited_subjects(subjects, recruitment_criteria):
    experiment = recruitment_criteria.subject_group.experiment
    participation_request_pseudonyms = ParticipationRequest.objects.filter(
        recruitment_criteria__subject_group__experiment=experiment,
        status=ParticipationRequest.STATUS.get_value('invited')
    ).values_list('pseudonym', flat=True)
    return subjects.exclude(pseudonym__in=participation_request_pseudonyms)
