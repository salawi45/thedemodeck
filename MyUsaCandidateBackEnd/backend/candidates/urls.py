from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CandidateViewSet,
    IssueViewSet,
    CandidateIssueViewSet,
    CandidateSimilarityViewSet,
    get_parties,
    get_ideologies,
    fetch_issues_from_wikidata,
    link_candidate_issues,
    get_candidate_issues_by_id,
)

# Create the router and register viewsets
router = DefaultRouter()
router.register(r'candidates', CandidateViewSet, basename='candidate')
router.register(r'issues', IssueViewSet, basename='issue')
router.register(r'candidate-issues', CandidateIssueViewSet, basename='candidateissue')
router.register(r'candidate-similarities', CandidateSimilarityViewSet, basename='candidatesimilarity')

# Define the full URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('parties/', get_parties, name='get_all_parties'),
    path('ideologies/', get_ideologies, name='get_all_ideologies'),
    path('fetch-issues/', fetch_issues_from_wikidata, name='fetch_issues'),
    path('link-candidate-issues/', link_candidate_issues, name='link_candidate_issues'),
    path('candidates/<int:id>/issues/', get_candidate_issues_by_id, name='get_candidate_issues'),
]
