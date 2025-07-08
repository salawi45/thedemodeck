from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create the router and register viewsets
router = DefaultRouter()
router.register(r'candidates', views.CandidateViewSet)
router.register(r'issues', views.IssueViewSet)
router.register(r'candidate-issues', views.CandidateIssueViewSet)
router.register(r'candidate-similarities', views.CandidateSimilarityViewSet)
router.register(r'bills', views.BillViewSet)
router.register(r'votes', views.VoteViewSet)

# Define the full URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('parties/', views.get_parties, name='get_parties'),
    path('ideologies/', views.get_ideologies, name='get_ideologies'),
    path('candidates/<int:id>/issues/', views.get_candidate_issues_by_id, name='get_candidate_issues'),
    path('candidate/<int:id>/similar/', views.get_similar_candidates, name='get_similar_candidates'),
    path('calculate-similarity/', views.calculate_similarity_scores, name='calculate_similarity_scores'),
    path('congress/bills/', views.get_recent_bills, name='get_recent_bills'),

    
    # New bill and vote endpoints
    path('update-bioguide-ids/', views.update_candidates_with_bioguide_ids, name='update_bioguide_ids'),
    path('fetch-bills/', views.fetch_bills_from_congress, name='fetch_bills'),
    path('fetch-votes/', views.fetch_votes_from_congress, name='fetch_votes'),
    path('candidates/<int:candidate_id>/bills/', views.get_candidate_bills, name='get_candidate_bills'),
    path('candidates/<int:candidate_id>/votes/', views.get_candidate_votes, name='get_candidate_votes'),
    path('bills/<str:bill_id>/votes/', views.get_bill_votes, name='get_bill_votes'),
    path('bills/by-bill-id/<str:bill_id>/', views.get_bill_by_bill_id, name='get_bill_by_bill_id'),
]
