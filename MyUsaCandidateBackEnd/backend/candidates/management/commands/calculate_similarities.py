from django.core.management.base import BaseCommand
from candidates.models import Candidate, CandidateIssue, CandidateSimilarity
from itertools import combinations

class Command(BaseCommand):
    help = 'Calculate similarity scores between candidates based on shared issues'

    def handle(self, *args, **options):
        self.stdout.write('Starting similarity calculation...')

        candidates = list(Candidate.objects.all())
        total_candidates = len(candidates)
        self.stdout.write(f'Found {total_candidates} candidates')

        # Clear existing similarities
        CandidateSimilarity.objects.all().delete()
        self.stdout.write('Cleared existing similarity scores')

        # Pre-fetch issues for all candidates to reduce DB hits
        candidate_issues_map = {}
        for candidate in candidates:
            issue_ids = set(
                CandidateIssue.objects.filter(candidate=candidate).values_list('issue_id', flat=True)
            )
            candidate_issues_map[candidate.id] = issue_ids

        pairs_processed = 0
        batch_size = 1000
        similarity_objects = []

        for candidate1, candidate2 in combinations(candidates, 2):
            issues1 = candidate_issues_map.get(candidate1.id, set())
            issues2 = candidate_issues_map.get(candidate2.id, set())

            if issues1 or issues2:
                intersection = len(issues1.intersection(issues2))
                union = len(issues1.union(issues2))
                similarity_score = intersection / union if union > 0 else 0

                if similarity_score > 0:
                    similarity_objects.append(
                        CandidateSimilarity(
                            candidate=candidate1,
                            similar=candidate2,
                            score=similarity_score
                        )
                    )
                    similarity_objects.append(
                        CandidateSimilarity(
                            candidate=candidate2,
                            similar=candidate1,
                            score=similarity_score
                        )
                    )

            pairs_processed += 1

            # Bulk insert in batches for performance
            if pairs_processed % batch_size == 0:
                CandidateSimilarity.objects.bulk_create(similarity_objects)
                similarity_objects = []
                self.stdout.write(f'Processed {pairs_processed} pairs...')

        # Insert any remaining objects
        if similarity_objects:
            CandidateSimilarity.objects.bulk_create(similarity_objects)

        self.stdout.write(self.style.SUCCESS(f'Successfully calculated similarities for {pairs_processed} candidate pairs'))
