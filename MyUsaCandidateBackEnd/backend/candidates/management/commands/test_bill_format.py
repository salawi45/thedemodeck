from django.core.management.base import BaseCommand
from django.conf import settings
from candidates.models import Bill
import requests


class Command(BaseCommand):
    help = 'Test different bill ID formats to find the correct one'

    def handle(self, *args, **options):
        self.stdout.write("Testing bill ID formats...")
        
        headers = {
            "X-Api-Key": settings.CONGRESS_API_KEY
        }
        
        # Get a few bills from our database
        bills = Bill.objects.all()[:5]
        
        for bill in bills:
            self.stdout.write(f"\nTesting bill: {bill.bill_id}")
            
            # Try different formats
            formats_to_test = [
                bill.bill_id,  # Current format: HR2808-118
                f"{bill.bill_type}{bill.bill_number}",  # HR2808
                f"{bill.bill_type}{bill.bill_number}-{bill.congress}",  # HR2808-118
                f"{bill.congress}/{bill.bill_type}{bill.bill_number}",  # 118/HR2808
                f"{bill.bill_type}{bill.bill_number}/{bill.congress}",  # HR2808/118
            ]
            
            for bill_format in formats_to_test:
                try:
                    url = f"https://api.congress.gov/v3/bill/{bill_format}"
                    self.stdout.write(f"  Testing: {url}")
                    
                    response = requests.get(url, headers=headers, params={'format': 'json'})
                    self.stdout.write(f"    Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        self.stdout.write(f"    SUCCESS! Found bill: {data.get('bill', {}).get('title', 'No title')[:50]}...")
                        self.stdout.write(f"    Bill keys: {list(data.get('bill', {}).keys())}")
                        if 'votes' in data.get('bill', {}):
                            self.stdout.write(f"    Has votes: {len(data['bill']['votes'])}")
                        break
                    else:
                        self.stdout.write(f"    Error: {response.text[:100]}...")
                        
                except Exception as e:
                    self.stdout.write(f"    Exception: {str(e)}")
        
        self.stdout.write(self.style.SUCCESS("Bill format testing completed")) 