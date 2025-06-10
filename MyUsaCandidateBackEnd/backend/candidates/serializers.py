from rest_framework import serializers
from .models import Candidate, Issue, CandidateIssue, CandidateSimilarity

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
