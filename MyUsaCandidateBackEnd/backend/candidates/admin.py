from django.contrib import admin
from .models import Candidate, Issue, CandidateIssue, CandidateSimilarity, Bill, Vote

# Register your models here.

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('label', 'party_qid', 'ideology_qid', 'bioguide_id', 'dob', 'last_updated')
    search_fields = ('label', 'party_qid', 'ideology_qid', 'bioguide_id')
    list_filter = ('party_qid', 'ideology_qid')
    readonly_fields = ('last_updated',)

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

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_id', 'title', 'congress', 'bill_type', 'sponsor', 'status', 'introduced_date', 'last_action_date')
    list_filter = ('congress', 'bill_type', 'status', 'introduced_date')
    search_fields = ('bill_id', 'title', 'sponsor__label', 'sponsor_bioguide_id')
    readonly_fields = ('last_updated',)
    date_hierarchy = 'introduced_date'
    list_per_page = 50
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('bill_id', 'congress', 'bill_type', 'bill_number', 'title', 'short_title')
        }),
        ('Sponsor Information', {
            'fields': ('sponsor_bioguide_id', 'sponsor')
        }),
        ('Content', {
            'fields': ('summary', 'congress_gov_url')
        }),
        ('Dates and Status', {
            'fields': ('introduced_date', 'last_action_date', 'last_action_text', 'status')
        }),
        ('System', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'bill', 'vote_position', 'vote_date', 'chamber', 'roll_call', 'congress')
    list_filter = ('vote_position', 'chamber', 'congress', 'vote_date')
    search_fields = ('candidate__label', 'bill__bill_id', 'bill__title')
    readonly_fields = ('vote_date',)
    date_hierarchy = 'vote_date'
    list_per_page = 100
    
    fieldsets = (
        ('Vote Information', {
            'fields': ('bill', 'candidate', 'vote_position', 'vote_date')
        }),
        ('Vote Context', {
            'fields': ('chamber', 'roll_call', 'congress', 'session')
        }),
    )
