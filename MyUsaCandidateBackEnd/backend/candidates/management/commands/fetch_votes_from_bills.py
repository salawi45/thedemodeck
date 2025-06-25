from django.core.management.base import BaseCommand
from django.conf import settings
from candidates.models import Bill, Vote, Candidate
import requests
import time


class Command(BaseCommand):
    help = 'Fetch votes from Congress.gov by getting them from individual bill endpoints'

    def add_arguments(self, parser):
        parser.add_argument(
            '--congress',
            type=int,
            default=118,
            help='Congress number (default: 118)',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Number of bills to process (default: 50)',
        )

    def handle(self, *args, **options):
        congress = options['congress']
        limit = options['limit']
        
        self.stdout.write(f"Fetching votes from bills for Congress {congress}...")
        
        # Get bills that don't have votes yet
        bills = Bill.objects.filter(congress=congress)[:limit]
        self.stdout.write(f"Processing {bills.count()} bills...")
        
        headers = {
            "X-Api-Key": settings.CONGRESS_API_KEY
        }
        
        total_votes_created = 0
        total_votes_updated = 0
        
        for i, bill in enumerate(bills, 1):
            try:
                self.stdout.write(f"Processing bill {i}/{bills.count()}: {bill.bill_id}")
                
                # Get bill details including votes
                bill_url = f"https://api.congress.gov/v3/bill/{bill.bill_id}"
                params = {
                    'format': 'json'
                }
                
                response = requests.get(bill_url, headers=headers, params=params)
                
                if response.status_code == 200:
                    bill_data = response.json()
                    
                    # Check if bill has votes
                    votes_data = bill_data.get('votes', [])
                    
                    if votes_data:
                        self.stdout.write(f"  Found {len(votes_data)} votes for {bill.bill_id}")
                        
                        for vote_data in votes_data:
                            try:
                                # Extract vote information
                                roll_call = vote_data.get('roll')
                                vote_date = vote_data.get('date')
                                chamber = vote_data.get('chamber')
                                session = vote_data.get('session')
                                
                                # Get individual vote positions
                                vote_positions = vote_data.get('votes', {})
                                
                                for position, voters in vote_positions.items():
                                    if position in ['Yes', 'No', 'Present', 'Not Voting']:
                                        for voter in voters:
                                            bioguide_id = voter.get('bioguideId')
                                            
                                            if bioguide_id:
                                                try:
                                                    # Find candidate by bioguide_id
                                                    candidate = Candidate.objects.get(bioguide_id=bioguide_id)
                                                    
                                                    # Create or update vote record
                                                    vote, created_flag = Vote.objects.update_or_create(
                                                        bill=bill,
                                                        candidate=candidate,
                                                        roll_call=roll_call,
                                                        defaults={
                                                            'vote_position': position,
                                                            'vote_date': vote_date,
                                                            'chamber': chamber,
                                                            'congress': congress,
                                                            'session': session,
                                                        }
                                                    )
                                                    
                                                    if created_flag:
                                                        total_votes_created += 1
                                                    else:
                                                        total_votes_updated += 1
                                                        
                                                except Candidate.DoesNotExist:
                                                    self.stdout.write(f"    Candidate with Bioguide ID {bioguide_id} not found")
                                                    continue
                            except Exception as e:
                                self.stdout.write(f"    Error processing vote {roll_call}: {str(e)}")
                                continue
                    else:
                        self.stdout.write(f"  No votes found for {bill.bill_id}")
                        
                else:
                    self.stdout.write(f"  Error fetching bill {bill.bill_id}: {response.status_code}")
                
                # Add a small delay to avoid hitting API rate limits
                time.sleep(0.1)
                
            except Exception as e:
                self.stdout.write(f"Error processing bill {bill.bill_id}: {str(e)}")
                continue
        
        self.stdout.write(self.style.SUCCESS(
            f"Successfully processed votes: {total_votes_created + total_votes_updated} total "
            f"(created: {total_votes_created}, updated: {total_votes_updated})"
        )) 