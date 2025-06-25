from django.core.management.base import BaseCommand
from candidates.models import Bill, Vote, Candidate
from datetime import date


class Command(BaseCommand):
    help = 'Create sample votes to demonstrate the functionality'

    def handle(self, *args, **options):
        self.stdout.write("Creating sample votes...")
        
        # Get some bills and candidates
        bills = Bill.objects.all()[:10]  # First 10 bills
        candidates = Candidate.objects.filter(bioguide_id__isnull=False)[:20]  # First 20 candidates with Bioguide IDs
        
        if not bills.exists():
            self.stdout.write("No bills found. Please fetch bills first.")
            return
            
        if not candidates.exists():
            self.stdout.write("No candidates with Bioguide IDs found. Please update candidates first.")
            return
        
        self.stdout.write(f"Found {bills.count()} bills and {candidates.count()} candidates with Bioguide IDs")
        
        vote_positions = ['Yes', 'No', 'Present', 'Not Voting']
        chambers = ['house', 'senate']
        
        created_votes = 0
        
        for i, bill in enumerate(bills):
            self.stdout.write(f"Creating votes for bill {i+1}: {bill.bill_id}")
            
            # Create 5-10 votes per bill
            num_votes = min(10, candidates.count())
            
            for j in range(num_votes):
                candidate = candidates[j]
                vote_position = vote_positions[j % len(vote_positions)]
                chamber = chambers[j % len(chambers)]
                
                try:
                    vote, created = Vote.objects.get_or_create(
                        bill=bill,
                        candidate=candidate,
                        roll_call=j + 1,
                        defaults={
                            'vote_position': vote_position,
                            'vote_date': date(2024, 1, 15 + j),  # Sample dates
                            'chamber': chamber,
                            'congress': bill.congress,
                            'session': 1,
                        }
                    )
                    
                    if created:
                        created_votes += 1
                        self.stdout.write(f"  Created vote: {candidate.label} voted {vote_position} on {bill.bill_id}")
                        
                except Exception as e:
                    self.stdout.write(f"  Error creating vote: {str(e)}")
                    continue
        
        self.stdout.write(self.style.SUCCESS(f"Successfully created {created_votes} sample votes"))
        self.stdout.write("You can now view these votes in the admin interface!") 