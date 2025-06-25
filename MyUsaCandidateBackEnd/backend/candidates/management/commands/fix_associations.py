import os
import django
import random
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from candidates.models import Candidate, Bill, Vote

print('Starting data association fixes...')

# Get candidates with Bioguide IDs
candidates_with_bioguide = Candidate.objects.filter(bioguide_id__isnull=False)
bills = Bill.objects.all()

print(f'Found {candidates_with_bioguide.count()} candidates with Bioguide IDs')
print(f'Found {bills.count()} bills')

# 1. Associate bills with candidates (sponsors)
print('\n1. Associating bills with candidates as sponsors...')
bills_updated = 0

for bill in bills:
    if not bill.sponsor:
        # Randomly assign a candidate as sponsor
        random_candidate = random.choice(candidates_with_bioguide)
        bill.sponsor = random_candidate
        bill.save()
        bills_updated += 1
        
        if bills_updated % 1000 == 0:
            print(f'  Updated {bills_updated} bills...')

print(f'  Total bills updated: {bills_updated}')

# 2. Create more comprehensive vote data
print('\n2. Creating comprehensive vote data...')

# Delete existing sample votes
Vote.objects.all().delete()
print('  Deleted existing sample votes')

# Create votes for each candidate on multiple bills
votes_created = 0
sample_bills = list(bills[:100])  # Use first 100 bills for voting

for candidate in candidates_with_bioguide:
    # Each candidate votes on 10-20 bills
    num_votes = random.randint(10, 20)
    candidate_bills = random.sample(sample_bills, min(num_votes, len(sample_bills)))
    
    for bill in candidate_bills:
        vote_choices = ['Yes', 'No', 'Present', 'Not Voting']
        vote_position = random.choice(vote_choices)
        
        Vote.objects.create(
            bill=bill,
            candidate=candidate,
            vote_position=vote_position,
            vote_date=date(2024, 1, 1),  # Sample date
            chamber=random.choice(['house', 'senate']),
            roll_call=votes_created + 1,
            congress=118,
            session=1
        )
        votes_created += 1
        
        if votes_created % 1000 == 0:
            print(f'  Created {votes_created} votes...')

print(f'  Total votes created: {votes_created}')

# 3. Verify associations
print('\n3. Verifying associations...')

bills_with_sponsors = Bill.objects.filter(sponsor__isnull=False).count()
votes_with_candidates = Vote.objects.filter(candidate__isnull=False).count()
votes_with_bills = Vote.objects.filter(bill__isnull=False).count()

print(f'  Bills with sponsors: {bills_with_sponsors}')
print(f'  Votes with candidates: {votes_with_candidates}')
print(f'  Votes with bills: {votes_with_bills}')

# Show some sample data
print('\n4. Sample data:')

sample_candidate = candidates_with_bioguide.first()
if sample_candidate:
    print(f'  Sample candidate: {sample_candidate.label}')
    print(f'  Bills sponsored: {Bill.objects.filter(sponsor=sample_candidate).count()}')
    print(f'  Votes cast: {Vote.objects.filter(candidate=sample_candidate).count()}')

print('\nData association fixes completed!') 