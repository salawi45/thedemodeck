from django.core.management.base import BaseCommand
from django.conf import settings
import requests


class Command(BaseCommand):
    help = 'Test different votes API endpoints to find the correct one'

    def handle(self, *args, **options):
        self.stdout.write("Testing different votes API endpoints...")
        
        headers = {
            "X-Api-Key": settings.CONGRESS_API_KEY
        }
        
        # Test different vote endpoints
        endpoints_to_test = [
            "https://api.congress.gov/v3/vote",
            "https://api.congress.gov/v3/votes", 
            "https://api.congress.gov/v3/rollcall",
            "https://api.congress.gov/v3/rollcalls",
        ]
        
        for url in endpoints_to_test:
            try:
                self.stdout.write(f"\nTesting: {url}")
                params = {
                    'congress': 118,
                    'format': 'json',
                    'limit': 5
                }
                
                response = requests.get(url, headers=headers, params=params)
                self.stdout.write(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    self.stdout.write(f"Response keys: {list(data.keys())}")
                    if 'votes' in data:
                        self.stdout.write(f"Number of votes: {len(data['votes'])}")
                        if data['votes']:
                            self.stdout.write(f"First vote keys: {list(data['votes'][0].keys())}")
                    elif 'rollcalls' in data:
                        self.stdout.write(f"Number of rollcalls: {len(data['rollcalls'])}")
                        if data['rollcalls']:
                            self.stdout.write(f"First rollcall keys: {list(data['rollcalls'][0].keys())}")
                else:
                    self.stdout.write(f"Error: {response.text[:200]}...")
                    
            except Exception as e:
                self.stdout.write(f"Exception: {str(e)}")
        
        # Test member-specific votes
        self.stdout.write("\n\nTesting member votes...")
        try:
            # Get a member first
            member_url = "https://api.congress.gov/v3/member"
            member_response = requests.get(member_url, headers=headers, params={'format': 'json', 'limit': 1})
            
            if member_response.status_code == 200:
                member_data = member_response.json()
                if member_data.get('members'):
                    member = member_data['members'][0]
                    bioguide_id = member.get('bioguideId')
                    
                    if bioguide_id:
                        self.stdout.write(f"Testing votes for member: {bioguide_id}")
                        
                        # Try different member vote endpoints
                        member_vote_urls = [
                            f"https://api.congress.gov/v3/member/{bioguide_id}/votes",
                            f"https://api.congress.gov/v3/member/{bioguide_id}/vote",
                        ]
                        
                        for vote_url in member_vote_urls:
                            try:
                                vote_response = requests.get(vote_url, headers=headers, params={'format': 'json', 'limit': 5})
                                self.stdout.write(f"Member votes {vote_url}: {vote_response.status_code}")
                                
                                if vote_response.status_code == 200:
                                    vote_data = vote_response.json()
                                    self.stdout.write(f"Response keys: {list(vote_data.keys())}")
                                    if 'votes' in vote_data:
                                        self.stdout.write(f"Number of votes: {len(vote_data['votes'])}")
                                        if vote_data['votes']:
                                            self.stdout.write(f"First vote keys: {list(vote_data['votes'][0].keys())}")
                            except Exception as e:
                                self.stdout.write(f"Member vote error: {str(e)}")
        except Exception as e:
            self.stdout.write(f"Member test error: {str(e)}")
        
        self.stdout.write(self.style.SUCCESS("Votes API testing completed")) 