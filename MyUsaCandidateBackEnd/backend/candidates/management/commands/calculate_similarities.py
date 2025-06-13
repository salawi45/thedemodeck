from django.core.management.base import BaseCommand
from candidates.models import Candidate, CandidateIssue, CandidateSimilarity
from itertools import combinations

class Command(BaseCommand):
    help = 'Calculate similarity scores between candidates based on shared issues'

    def handle(self, *args, **options):
        self.stdout.write('Starting similarity calculation...')
        
        # Get all candidates
        candidates = Candidate.objects.all()
        total_candidates = candidates.count()
        self.stdout.write(f'Found {total_candidates} candidates')
        
        # Clear existing similarity scores
        CandidateSimilarity.objects.all().delete()
        self.stdout.write('Cleared existing similarity scores')
        
        # For each pair of candidates
        pairs_processed = 0
        for candidate1, candidate2 in combinations(candidates, 2):
            # Get their issues
            issues1 = set(CandidateIssue.objects.filter(candidate=candidate1).values_list('issue_id', flat=True))
            issues2 = set(CandidateIssue.objects.filter(candidate=candidate2).values_list('issue_id', flat=True))
            
            # Calculate Jaccard similarity
            if issues1 or issues2:  # Only calculate if at least one candidate has issues
                intersection = len(issues1.intersection(issues2))
                union = len(issues1.union(issues2))
                similarity_score = intersection / union if union > 0 else 0
                
                # Create similarity records in both directions
                CandidateSimilarity.objects.create(
                    candidate=candidate1,
                    similar=candidate2,
                    score=similarity_score
                )
                CandidateSimilarity.objects.create(
                    candidate=candidate2,
                    similar=candidate1,
                    score=similarity_score
                )
            
            pairs_processed += 1
            if pairs_processed % 100 == 0:
                self.stdout.write(f'Processed {pairs_processed} pairs...')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully calculated similarities for {pairs_processed} candidate pairs')) 