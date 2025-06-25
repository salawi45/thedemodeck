from django.core.management.base import BaseCommand
from django.conf import settings
from candidates.models import Candidate, Bill, Vote
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
from datetime import datetime


class Command(BaseCommand):
    help = 'Fetch bills and votes from Congress.gov API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--update-bioguide-ids',
            action='store_true',
            help='Update candidates with Bioguide IDs from Wikidata',
        )
        parser.add_argument(
            '--fetch-bills',
            action='store_true',
            help='Fetch bills from Congress.gov',
        )
        parser.add_argument(
            '--fetch-votes',
            action='store_true',
            help='Fetch votes from Congress.gov',
        )
        parser.add_argument(
            '--congress',
            type=int,
            default=118,
            help='Congress number (default: 118)',
        )
        parser.add_argument(
            '--chamber',
            type=str,
            default='house',
            choices=['house', 'senate'],
            help='Chamber to fetch votes from (default: house)',
        )

    def handle(self, *args, **options):
        if options['update_bioguide_ids']:
            self.update_bioguide_ids()
        
        if options['fetch_bills']:
            self.fetch_bills(options['congress'])
        
        if options['fetch_votes']:
            self.fetch_votes(options['congress'], options['chamber'])

    def update_bioguide_ids(self):
        """Update candidates with their Bioguide IDs from Wikidata"""
        self.stdout.write("Updating candidates with Bioguide IDs...")
        
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery("""
        SELECT ?candidate ?candidateLabel ?bioguideId WHERE {
            ?candidate wdt:P31 wd:Q5;          # instance of human
                 wdt:P106 wd:Q82955;     # occupation: politician
                 wdt:P27 wd:Q30;         # country: United States
                 wdt:P1157 ?bioguideId.  # US Congress Bio ID

            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        updated = 0
        for result in results["results"]["bindings"]:
            candidate_qid = result["candidate"]["value"].split("/")[-1]
            bioguide_id = result["bioguideId"]["value"]
            candidate_label = result.get("candidateLabel", {}).get("value", "Unknown")

            try:
                candidate = Candidate.objects.get(cqid=candidate_qid)
                candidate.bioguide_id = bioguide_id
                candidate.save()
                updated += 1
                self.stdout.write(f"Updated {candidate_label} with Bioguide ID: {bioguide_id}")
            except Candidate.DoesNotExist:
                self.stdout.write(f"Candidate {candidate_qid} not found in database")
            except Exception as e:
                self.stdout.write(f"Error updating {candidate_qid}: {str(e)}")

        self.stdout.write(self.style.SUCCESS(f"Successfully updated {updated} candidates"))

    def fetch_bills(self, congress):
        """Fetch bills from Congress.gov API"""
        self.stdout.write(f"Fetching ALL bills for Congress {congress}...")
        
        url = "https://api.congress.gov/v3/bill"
        headers = {
            "X-Api-Key": settings.CONGRESS_API_KEY
        }
        
        # Start with House bills (hr), then Senate bills (s), then other types
        bill_types = ['hr', 's', 'hjres', 'sjres', 'hconres', 'sconres', 'hres', 'sres']
        
        total_created = 0
        total_updated = 0
        
        for bill_type in bill_types:
            self.stdout.write(f"\nFetching {bill_type.upper()} bills...")
            
            params = {
                'congress': congress,
                'billType': bill_type,
                'format': 'json',
                'limit': 250  # Maximum allowed per request
            }
            
            page = 1
            has_more_pages = True
            
            while has_more_pages:
                try:
                    params['offset'] = (page - 1) * params['limit']
                    self.stdout.write(f"Fetching page {page} for {bill_type.upper()} bills...")
                    
                    response = requests.get(url, headers=headers, params=params)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Debug: Print the response structure for first page
                    if page == 1:
                        self.stdout.write(f"API Response keys: {list(data.keys())}")
                        if 'bills' in data:
                            self.stdout.write(f"Number of bills in first page: {len(data['bills'])}")
                            if data['bills']:
                                self.stdout.write(f"First bill structure: {list(data['bills'][0].keys())}")
                    
                    bills = data.get('bills', [])
                    if not bills:
                        self.stdout.write(f"No more bills found for {bill_type.upper()}")
                        break
                    
                    created = updated = 0
                    for bill_data in bills:
                        try:
                            # Extract bill information - handle the correct API structure
                            bill_type_code = bill_data.get('type', '')
                            bill_number = bill_data.get('number', '')
                            
                            # Construct bill_id from type and number
                            bill_id = f"{bill_type_code}{bill_number}-{congress}" if bill_type_code and bill_number else None
                            
                            # Skip if we can't construct a valid bill_id
                            if not bill_id:
                                self.stdout.write(f"Skipping bill with invalid type/number: {bill_data.get('title', 'Unknown')[:50]}...")
                                continue
                            
                            title = bill_data.get('title', '')
                            
                            # Extract sponsor information - this might need to be fetched separately
                            # For now, we'll leave sponsor fields empty and update them later
                            sponsor_bioguide_id = None
                            sponsor_candidate = None
                            
                            # Extract dates and actions
                            latest_action = bill_data.get('latestAction', {})
                            last_action_date = latest_action.get('actionDate')
                            last_action_text = latest_action.get('text', '')
                            
                            # Parse bill ID components
                            bill_type_short = bill_type_code[:2] if bill_type_code else ''
                            bill_number_int = int(bill_number) if bill_number.isdigit() else 0
                            
                            # Create or update bill
                            bill, created_flag = Bill.objects.update_or_create(
                                bill_id=bill_id,
                                defaults={
                                    'congress': congress,
                                    'bill_type': bill_type_short,
                                    'bill_number': bill_number_int,
                                    'title': title,
                                    'short_title': '',  # Will be updated when we fetch full bill details
                                    'summary': '',  # Will be updated when we fetch full bill details
                                    'sponsor_bioguide_id': sponsor_bioguide_id,
                                    'sponsor': sponsor_candidate,
                                    'introduced_date': None,  # Will be updated when we fetch full bill details
                                    'last_action_date': last_action_date,
                                    'last_action_text': last_action_text,
                                    'status': latest_action.get('actionBy', ''),
                                    'congress_gov_url': bill_data.get('url', ''),
                                }
                            )
                            
                            if created_flag:
                                created += 1
                            else:
                                updated += 1
                                
                        except Exception as e:
                            self.stdout.write(f"Error processing bill {bill_id}: {str(e)}")
                            continue
                    
                    self.stdout.write(f"Page {page}: Created {created}, Updated {updated} bills")
                    total_created += created
                    total_updated += updated
                    
                    # Check if there are more pages
                    pagination = data.get('pagination', {})
                    if pagination.get('next') is None:
                        has_more_pages = False
                    else:
                        page += 1
                        
                except requests.RequestException as e:
                    self.stdout.write(f"Error fetching page {page} for {bill_type}: {str(e)}")
                    break
                except Exception as e:
                    self.stdout.write(f"Unexpected error on page {page} for {bill_type}: {str(e)}")
                    break
            
            self.stdout.write(f"Completed {bill_type.upper()} bills. Total so far: {total_created + total_updated}")
        
        self.stdout.write(self.style.SUCCESS(f"Successfully processed ALL bills: {total_created + total_updated} total (created: {total_created}, updated: {total_updated})"))

    def fetch_votes(self, congress, chamber):
        """Fetch votes from Congress.gov API"""
        self.stdout.write(f"Fetching votes for Congress {congress}, Chamber: {chamber}...")
        
        # The correct endpoint for votes might be different
        # Let's try the member votes endpoint instead
        url = f"https://api.congress.gov/v3/member"
        headers = {
            "X-Api-Key": settings.CONGRESS_API_KEY
        }
        
        # First, let's get some members and their votes
        try:
            self.stdout.write("Getting members first...")
            members_response = requests.get(url, headers=headers, params={'format': 'json', 'limit': 10})
            members_response.raise_for_status()
            members_data = members_response.json()
            
            self.stdout.write(f"Members API Response keys: {list(members_data.keys())}")
            if 'members' in members_data:
                self.stdout.write(f"Number of members: {len(members_data['members'])}")
                
                created = updated = 0
                for member in members_data['members'][:5]:  # Process first 5 members
                    bioguide_id = member.get('bioguideId')
                    if not bioguide_id:
                        continue
                        
                    # Get votes for this member
                    member_votes_url = f"{url}/{bioguide_id}/votes"
                    votes_params = {
                        'congress': congress,
                        'chamber': chamber,
                        'format': 'json',
                        'limit': 20
                    }
                    
                    try:
                        self.stdout.write(f"Getting votes for member {bioguide_id}...")
                        votes_response = requests.get(member_votes_url, headers=headers, params=votes_params)
                        votes_response.raise_for_status()
                        votes_data = votes_response.json()
                        
                        self.stdout.write(f"Votes API Response keys: {list(votes_data.keys())}")
                        if 'votes' in votes_data:
                            self.stdout.write(f"Number of votes for {bioguide_id}: {len(votes_data['votes'])}")
                            
                            for vote_data in votes_data['votes']:
                                try:
                                    # Extract vote information
                                    roll_call = vote_data.get('roll')
                                    vote_date = vote_data.get('date')
                                    chamber_code = vote_data.get('chamber')
                                    session = vote_data.get('session')
                                    vote_position = vote_data.get('position')
                                    
                                    # Get bill information
                                    bill_data = vote_data.get('bill', {})
                                    bill_type = bill_data.get('type', '')
                                    bill_number = bill_data.get('number', '')
                                    bill_id = f"{bill_type}{bill_number}-{congress}" if bill_type and bill_number else None
                                    
                                    if not bill_id:
                                        self.stdout.write(f"Skipping vote {roll_call} - no associated bill")
                                        continue
                                    
                                    # Get or create bill
                                    try:
                                        bill = Bill.objects.get(bill_id=bill_id)
                                    except Bill.DoesNotExist:
                                        # Create a minimal bill record if it doesn't exist
                                        bill = Bill.objects.create(
                                            bill_id=bill_id,
                                            congress=congress,
                                            bill_type=bill_type[:2] if bill_type else '',
                                            bill_number=int(bill_number) if bill_number.isdigit() else 0,
                                            title=f"Bill {bill_id}",
                                        )
                                        self.stdout.write(f"Created minimal bill record: {bill_id}")
                                    
                                    # Find candidate by bioguide_id
                                    try:
                                        candidate = Candidate.objects.get(bioguide_id=bioguide_id)
                                        
                                        # Create or update vote record
                                        vote, created_flag = Vote.objects.update_or_create(
                                            bill=bill,
                                            candidate=candidate,
                                            roll_call=roll_call,
                                            defaults={
                                                'vote_position': vote_position,
                                                'vote_date': vote_date,
                                                'chamber': chamber_code,
                                                'congress': congress,
                                                'session': session,
                                            }
                                        )
                                        
                                        if created_flag:
                                            created += 1
                                        else:
                                            updated += 1
                                            
                                    except Candidate.DoesNotExist:
                                        self.stdout.write(f"Candidate with Bioguide ID {bioguide_id} not found")
                                        continue
                                        
                                except Exception as e:
                                    self.stdout.write(f"Error processing vote {roll_call}: {str(e)}")
                                    continue
                                    
                    except requests.RequestException as e:
                        self.stdout.write(f"Failed to get votes for member {bioguide_id}: {str(e)}")
                        continue
                
                self.stdout.write(self.style.SUCCESS(f"Successfully processed {created + updated} votes (created: {created}, updated: {updated})"))
                
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Failed to fetch members: {str(e)}"))
            if hasattr(e, 'response') and e.response is not None:
                self.stdout.write(f"Response status: {e.response.status_code}")
                self.stdout.write(f"Response content: {e.response.text[:500]}...") 