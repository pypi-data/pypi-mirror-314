from django.urls import include, path
from rest_framework_nested.routers import NestedDefaultRouter

from huscy.project_design.urls import experiment_router
from huscy.recruitment import views


experiment_router.register('subjectgroups', views.SubjectGroupViewset, basename='subjectgroup')

subject_group_router = NestedDefaultRouter(experiment_router, 'subjectgroups',
                                           lookup='subjectgroup')
subject_group_router.register('recruitmentcriteria', views.RecruitmentCriteriaViewSet)


urlpatterns = [
    path('api/', include(experiment_router.urls)),
    path('api/', include(subject_group_router.urls)),
]
