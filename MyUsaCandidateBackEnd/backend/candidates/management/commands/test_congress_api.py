from django.core.management.base import BaseCommand
from django.conf import settings
import requests


class Command(BaseCommand):
    help = 'Test Congress.gov API connection'

    def handle(self, *args, **options):
        self.stdout.write("Testing Congress.gov API connection...")
        
        # Test bills endpoint
        bills_url = "https://api.congress.gov/v3/bill"
        headers = {
            "X-Api-Key": settings.CONGRESS_API_KEY
        }
        
        params = {
            'congress': 118,
            'billType': 'hr',
            'format': 'json',
            'limit': 5
        }

        try:
            self.stdout.write(f"Testing bills endpoint: {bills_url}")
            response = requests.get(bills_url, headers=headers, params=params)
            self.stdout.write(f"Bills API Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.stdout.write(f"Bills API Response keys: {list(data.keys())}")
                if 'bills' in data:
                    self.stdout.write(f"Number of bills returned: {len(data['bills'])}")
                    if data['bills']:
                        first_bill = data['bills'][0]
                        self.stdout.write(f"First bill keys: {list(first_bill.keys())}")
                        self.stdout.write(f"First bill ID: {first_bill.get('billId')}")
                        self.stdout.write(f"First bill title: {first_bill.get('title', 'No title')[:100]}...")
            else:
                self.stdout.write(f"Bills API Error: {response.text[:200]}...")
                
        except Exception as e:
            self.stdout.write(f"Bills API Error: {str(e)}")

        # Test votes endpoint
        votes_urls = [
            "https://api.congress.gov/v3/vote",
            "https://api.congress.gov/v3/votes",
        ]
        
        for url in votes_urls:
            try:
                self.stdout.write(f"\nTesting votes endpoint: {url}")
                response = requests.get(url, headers=headers, params=params)
                self.stdout.write(f"Votes API Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    self.stdout.write(f"Votes API Response keys: {list(data.keys())}")
                    if 'votes' in data:
                        self.stdout.write(f"Number of votes returned: {len(data['votes'])}")
                        if data['votes']:
                            first_vote = data['votes'][0]
                            self.stdout.write(f"First vote keys: {list(first_vote.keys())}")
                            self.stdout.write(f"First vote roll: {first_vote.get('roll')}")
                else:
                    self.stdout.write(f"Votes API Error: {response.text[:200]}...")
                    
            except Exception as e:
                self.stdout.write(f"Votes API Error: {str(e)}")

        self.stdout.write(self.style.SUCCESS("API testing completed")) 