from rest_framework import serializers
from .models import Candidate, Issue, CandidateIssue, CandidateSimilarity, Bill, Vote

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class CandidateIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateIssue
        fields = '__all__'


class CandidateSimilaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateSimilarity
        fields = '__all__'


class BillSerializer(serializers.ModelSerializer):
    sponsor_name = serializers.CharField(source='sponsor.label', read_only=True)
    
    class Meta:
        model = Bill
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.label', read_only=True)
    bill_title = serializers.CharField(source='bill.title', read_only=True)
    bill_id = serializers.CharField(source='bill.bill_id', read_only=True)
    
    class Meta:
        model = Vote
        fields = '__all__'
