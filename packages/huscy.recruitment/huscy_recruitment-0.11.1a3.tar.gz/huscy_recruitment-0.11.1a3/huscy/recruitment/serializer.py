from rest_framework import serializers

# from huscy.appointments.serializers import AppointmentSerializer
from huscy.recruitment import models, services
# from huscy.recruitment.models import Recall
# from huscy.recruitment.services import create_or_update_participation_request


class ParticipationRequestSerializer(serializers.ModelSerializer):
    appointment = serializers.DateTimeField(required=False)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    timeslots = serializers.ListField(required=False, child=serializers.IntegerField(min_value=1))
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.ParticipationRequest
        fields = (
            'appointment',
            'attribute_filterset',
            'id',
            'status',
            'status_display',
            'timeslots',
            'user',
        )
        read_only_fields = 'attribute_filterset',

    """
    def create(self, validated_data):
        attribute_filterset = self.context.get('attribute_filterset')
        subject = self.context.get('subject')

        return create_or_update_participation_request(subject, attribute_filterset,
                                                      **validated_data)

    def to_representation(self, participation_request):
        response = super().to_representation(participation_request)
        if participation_request.status == models.ParticipationRequest.STATUS.get_value('pending'):
            try:
                recall = participation_request.recall.get()
            except Recall.DoesNotExist:
                return response

            # TODO: skip this, if appointment is in the past
            response['recall_appointment'] = AppointmentSerializer(recall.appointment).data
        return response
    """


class RecruitmentCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecruitmentCriteria
        fields = (
            'id',
            'attribute_filterset',
            'maximum_age_in_months',
            'minimum_age_in_months',
        )

    def update(self, recruitment_criteria, validated_data):
        subject_group = self.context.get('subject_group')
        return services.update_recruitment_criteria(subject_group, **validated_data)


class SubjectGroupSerializer(serializers.ModelSerializer):
    recruitment_criteria = RecruitmentCriteriaSerializer(many=True, read_only=True)

    class Meta:
        model = models.SubjectGroup
        fields = (
            'id',
            'description',
            'experiment',
            'name',
            'order',
            'recruitment_criteria',
        )
        read_only_fields = ('experiment', )

    def create(self, validated_data):
        experiment = self.context['experiment']
        return services.create_subject_group(experiment, **validated_data)
