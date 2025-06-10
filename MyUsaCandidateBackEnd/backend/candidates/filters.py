# candidates/filters.py
import django_filters
from datetime import date
from .models import Candidate

class CandidateFilter(django_filters.FilterSet):
    min_age = django_filters.NumberFilter(method='filter_min_age')
    max_age = django_filters.NumberFilter(method='filter_max_age')

    class Meta:
        model = Candidate
        fields = ['party_qid', 'ideology_qid']

    def filter_min_age(self, queryset, name, value):
        today = date.today()
        min_dob = date(today.year - value, today.month, today.day)
        return queryset.filter(dob__lte=min_dob)

    def filter_max_age(self, queryset, name, value):
        today = date.today()
        max_dob = date(today.year - value, today.month, today.day)
        return queryset.filter(dob__gte=max_dob)