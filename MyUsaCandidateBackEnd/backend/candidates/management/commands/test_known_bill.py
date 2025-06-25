from django.core.management.base import BaseCommand
from django.conf import settings
import requests


class Command(BaseCommand):
    help = 'Test with known bill IDs to find the correct format'

    def handle(self, *args, **options):
        self.stdout.write("Testing with known bill IDs...")
        
        headers = {
            "X-Api-Key": settings.CONGRESS_API_KEY
        }
        
        # Test with some known bill IDs from Congress.gov
        known_bills = [
            "hr1-118",  # Lowercase with dash
            "HR1-118",  # Uppercase with dash
            "hr1/118",  # With slash
            "118/hr1",  # Congress first
            "hr1",      # Just bill number
            "s1-118",   # Senate bill
            "s1",       # Senate bill without congress
        ]
        
        for bill_id in known_bills:
            try:
                url = f"https://api.congress.gov/v3/bill/{bill_id}"
                self.stdout.write(f"\nTesting: {url}")
                
                response = requests.get(url, headers=headers, params={'format': 'json'})
                self.stdout.write(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    bill_data = data.get('bill', {})
                    self.stdout.write(f"SUCCESS! Found bill: {bill_data.get('title', 'No title')[:100]}...")
                    self.stdout.write(f"Bill ID in response: {bill_data.get('billId', 'No ID')}")
                    self.stdout.write(f"Bill keys: {list(bill_data.keys())}")
                    
                    # Check for votes
                    if 'votes' in bill_data:
                        votes = bill_data['votes']
                        self.stdout.write(f"Has votes: {len(votes)}")
                        if votes:
                            first_vote = votes[0]
                            self.stdout.write(f"First vote keys: {list(first_vote.keys())}")
                            self.stdout.write(f"First vote roll: {first_vote.get('roll')}")
                            self.stdout.write(f"First vote date: {first_vote.get('date')}")
                    else:
                        self.stdout.write("No votes found")
                    break
                else:
                    self.stdout.write(f"Error: {response.text[:100]}...")
                    
            except Exception as e:
                self.stdout.write(f"Exception: {str(e)}")
        
        self.stdout.write(self.style.SUCCESS("Known bill testing completed")) 