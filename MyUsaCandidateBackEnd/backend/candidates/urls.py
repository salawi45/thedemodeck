from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create the router and register viewsets
router = DefaultRouter()
router.register(r'candidates', views.CandidateViewSet)
router.register(r'issues', views.IssueViewSet)
router.register(r'candidate-issues', views.CandidateIssueViewSet)
router.register(r'candidate-similarities', views.CandidateSimilarityViewSet)

# Define the full URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('parties/', views.get_parties, name='get_parties'),
    path('ideologies/', views.get_ideologies, name='get_ideologies'),
    path('candidates/<int:id>/issues/', views.get_candidate_issues_by_id, name='get_candidate_issues'),
    path('candidate/<int:id>/similar/', views.get_similar_candidates, name='get_similar_candidates'),
    path('calculate-similarity/', views.calculate_similarity_scores, name='calculate_similarity_scores'),
]
