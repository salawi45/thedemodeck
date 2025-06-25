import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from candidates.models import Candidate, Bill, Vote

print(f'Candidates: {Candidate.objects.count()}')
print(f'Bills: {Bill.objects.count()}')
print(f'Votes: {Vote.objects.count()}')
print(f'Candidates with Bioguide IDs: {Candidate.objects.filter(bioguide_id__isnull=False).count()}')

# Check some sample data
print(f'\nSample candidates with Bioguide IDs:')
candidates_with_bioguide = Candidate.objects.filter(bioguide_id__isnull=False)[:5]
for candidate in candidates_with_bioguide:
    print(f'  {candidate.name} - Bioguide ID: {candidate.bioguide_id}')

print(f'\nSample bills:')
bills = Bill.objects.all()[:5]
for bill in bills:
    print(f'  {bill.bill_id} - {bill.title[:50]}...')

print(f'\nSample votes:')
votes = Vote.objects.all()[:5]
for vote in votes:
    print(f'  {vote.vote_id} - {vote.bill.bill_id if vote.bill else "No bill"} - {vote.candidate.name if vote.candidate else "No candidate"}') 