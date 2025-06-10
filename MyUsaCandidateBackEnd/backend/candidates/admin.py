from django.contrib import admin
from .models import Candidate, Issue, CandidateIssue, CandidateSimilarity

# Register your models here.

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('label', 'party_qid', 'ideology_qid', 'dob', 'last_updated')
    search_fields = ('label', 'party_qid', 'ideology_qid')
    list_filter = ('party_qid',)

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('issue_qid', 'issue_label')
    search_fields = ('issue_qid', 'issue_label')

@admin.register(CandidateIssue)
class CandidateIssueAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'issue')
    search_fields = ('candidate__label', 'issue__issue_label')

@admin.register(CandidateSimilarity)
class CandidateSimilarityAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'similar', 'score')
    search_fields = ('candidate__label', 'similar__label')
    list_filter = ('score',)
