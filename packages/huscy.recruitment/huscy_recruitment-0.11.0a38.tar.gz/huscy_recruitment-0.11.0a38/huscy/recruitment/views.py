from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets
# from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

from huscy.project_design.models import Experiment
from huscy.recruitment.models import RecruitmentCriteria, SubjectGroup
from huscy.recruitment.serializer import (
    ParticipationRequestSerializer,
    RecruitmentCriteriaSerializer,
    SubjectGroupSerializer,
)
from huscy.recruitment.services import (
    # apply_attribute_filterset,
    delete_subject_group,
    get_subject_groups,
    # get_participation_requests_for_experiment,
)
from huscy.subjects.models import Subject
# from huscy.subjects.serializers import SubjectSerializer


'''
class ExperimentViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Experiment.objects.all()

    @action(detail=True, methods=['get'])
    def participation_requests(self, request, pk=None):
        experiment = self.get_object()
        participation_requests = get_participation_requests_for_experiment(experiment)
        return Response(data=ParticipationRequestSerializer(participation_requests, many=True).data)
'''


class SubjectGroupViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = SubjectGroupSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.experiment = get_object_or_404(Experiment, pk=self.kwargs['experiment_pk'])

    def get_queryset(self):
        return get_subject_groups(self.experiment)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['experiment'] = self.experiment
        return context

    def perform_destroy(self, subject_group):
        delete_subject_group(subject_group)


class RecruitmentCriteriaViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = RecruitmentCriteria.objects.all()
    serializer_class = RecruitmentCriteriaSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.experiment = get_object_or_404(Experiment, pk=self.kwargs['experiment_pk'])
        self.subject_group = get_object_or_404(SubjectGroup, pk=self.kwargs['subjectgroup_pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['experiment'] = self.experiment
        context['subject_group'] = self.subject_group
        return context

    """
    @action(detail=True, methods=['get'])
    def apply(self, request, pk=None):
        user = self.request.user
        attribute_filterset = self.get_object()
        subjects = apply_attribute_filterset(
            attribute_filterset,
            include_children=user.has_perm('subjects.view_child'),
            include_patients=user.has_perm('subjects.view_patient')
        )
        return Response(data=SubjectSerializer(subjects, many=True).data)
    """


class ParticipationRequestViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Subject.objects.all()
    serializer_class = ParticipationRequestSerializer

    """
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['attribute_filterset'] = get_object_or_404(AttributeFilterSet,
                                                           pk=self.kwargs['attributefilterset_pk'])
        context['subject'] = self.get_object()
        return context

    @action(detail=True, methods=['put'])
    def not_reached(self, request, pk, attributefilterset_pk):
        data = dict(status=ParticipationRequest.STATUS.get_value('pending'))
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    @action(detail=True, methods=['put'])
    def recall(self, request, pk, attributefilterset_pk):
        data = request.data.copy()
        data['status'] = ParticipationRequest.STATUS.get_value('pending')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    @action(detail=True, methods=['put'])
    def invited(self, request, pk, attributefilterset_pk):
        data = dict(status=ParticipationRequest.STATUS.get_value('invited'))
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
    """
