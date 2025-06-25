# candidates/views.py
# In your Django views.py
from rest_framework.decorators import api_view
from django.db.models import Q
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date
from SPARQLWrapper import SPARQLWrapper, JSON
from .models import Candidate, Issue, CandidateIssue, CandidateSimilarity, Bill, Vote
from .serializers import CandidateSerializer, IssueSerializer, CandidateIssueSerializer, CandidateSimilaritySerializer, BillSerializer, VoteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import CandidateFilter
from django.http import JsonResponse 
from django.conf import settings
import requests
import django_filters
from django.db.models import Count
from itertools import combinations


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['party_qid', 'ideology_qid']  # These will now filter by string values
    search_fields = ['label', 'description', 'party_qid', 'ideology_qid']
    ordering_fields = ['label', 'dob', 'last_updated']
    # In your Django views.py

    @action(detail=True, methods=['get'])
    def bills(self, request, pk=None):
        """Get bills sponsored by a candidate"""
        candidate = self.get_object()
        bills = Bill.objects.filter(sponsor=candidate)
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def votes(self, request, pk=None):
        """Get voting record for a candidate"""
        candidate = self.get_object()
        votes = Vote.objects.filter(candidate=candidate).select_related('bill')
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)

    # @action(detail=False, methods=['post'])
    # def fetch_from_wikidata(self, request):
    #     sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    #     sparql.setQuery("""
    #     SELECT ?item ?itemLabel ?party ?partyLabel ?ideology ?ideologyLabel ?dob ?description ?image WHERE {
    #       ?item wdt:P31 wd:Q5;          # instance of human
    #             wdt:P106 wd:Q82955;     # occupation: politician
    #             wdt:P27 wd:Q30.         # country: United States

    #       OPTIONAL { ?item wdt:P102 ?party. }
    #       OPTIONAL { ?item wdt:P1142 ?ideology. }
    #       OPTIONAL { ?item wdt:P569 ?dob. }
    #       OPTIONAL { ?item schema:description ?description. FILTER(LANG(?description)="en") }
    #       OPTIONAL { ?item wdt:P18 ?image. }

    #       SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    #     }
    #     """)
    #     sparql.setReturnFormat(JSON)
    #     results = sparql.query().convert()

    #     created = updated = 0
    #     for result in results["results"]["bindings"]:
    #         qid = result["item"]["value"].split("/")[-1]
    #         label = result["itemLabel"]["value"]
    #         party_qid = result.get("party", {}).get("value", "").split("/")[-1] if "party" in result else None
    #         ideology_qid = result.get("ideology", {}).get("value", "").split("/")[-1] if "ideology" in result else None
    #         dob = result.get("dob", {}).get("value", None)
    #         photo_url = result.get("image", {}).get("value", "")
    #         description = result.get("description", {}).get("value", "")

    #         candidate, created_flag = Candidate.objects.update_or_create(
    #             cqid=qid,
    #             defaults={
    #                 "label": label,
    #                 "party_qid": party_qid,
    #                 "ideology_qid": ideology_qid,
    #                 "dob": dob,
    #                 "photo_url": photo_url,
    #                 "description": description,
    #                 "last_updated": now()
    #             }
    #         )
    #         if created_flag:
    #             created += 1
    #         else:
    #             updated += 1

    #     return Response({"created": created, "updated": updated})
    
@api_view(['GET'])
def get_parties(request):
    """Get unique party values for filtering"""
    parties = Candidate.objects.values_list('party_qid', flat=True).distinct()
    parties = [p for p in parties if p]  # Remove None values
    return Response(parties)

@api_view(['GET'])
def get_ideologies(request):
    """Get unique ideology values for filtering"""
    ideologies = Candidate.objects.values_list('ideology_qid', flat=True).distinct()
    ideologies = [i for i in ideologies if i]  # Remove None values
    return Response(ideologies)




class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class CandidateIssueViewSet(viewsets.ModelViewSet):
    queryset = CandidateIssue.objects.all()
    serializer_class = CandidateIssueSerializer


class CandidateSimilarityViewSet(viewsets.ModelViewSet):
    queryset = CandidateSimilarity.objects.all()
    serializer_class = CandidateSimilaritySerializer

    # fetch_from_wikidata remains the same


# Similarly you can add filter/search on other ViewSets if needed

class CandidateFilter(django_filters.FilterSet):
    min_age = django_filters.NumberFilter(method='filter_min_age')
    max_age = django_filters.NumberFilter(method='filter_max_age')

    class Meta:
        model = Candidate
        fields = ['party_qid', 'ideology_qid']

    def filter_min_age(self, queryset, name, value):
        today = date.today()
        min_dob = date(today.year - value, today.month, today.day)
        return queryset.filter(dob__lte=min_dob)

    def filter_max_age(self, queryset, name, value):
        today = date.today()
        max_dob = date(today.year - value, today.month, today.day)
        return queryset.filter(dob__gte=max_dob)

@api_view(['POST'])
def fetch_issues_from_wikidata(request):
    """Fetch issues from Wikidata and link them to candidates"""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    
    # Query to get specific political issues and their labels
    sparql.setQuery("""
    SELECT DISTINCT ?issue ?issueLabel WHERE {
        {
            # Get issues that are political topics
            ?issue wdt:P31 wd:Q18616576.  # instance of political issue
        } UNION {
            # Get specific political issues directly
            VALUES ?issue {
                wd:Q16917    # Gun control
                wd:Q13330    # Abortion
                wd:Q13330    # Climate change
                wd:Q13330    # Healthcare
                wd:Q13330    # Immigration
                wd:Q13330    # Education
                wd:Q13330    # Economy
                wd:Q13330    # Foreign policy
                wd:Q13330    # National security
                wd:Q13330    # Social security
                wd:Q13330    # Tax reform
                wd:Q13330    # Infrastructure
                wd:Q13330    # Energy policy
                wd:Q13330    # Environmental protection
                wd:Q13330    # Civil rights
                wd:Q13330    # Labor rights
                wd:Q13330    # Trade policy
                wd:Q13330    # Welfare
                wd:Q13330    # Veterans affairs
                wd:Q13330    # Drug policy
            }
        }
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    created = 0
    for result in results["results"]["bindings"]:
        issue_qid = result["issue"]["value"].split("/")[-1]
        issue_label = result["issueLabel"]["value"]

        # Create or update the issue
        issue, _ = Issue.objects.update_or_create(
            issue_qid=issue_qid,
            defaults={
                "issue_label": issue_label
            }
        )
        created += 1

    return Response({"created": created})

@api_view(['POST'])
def link_candidate_issues(request):
    """Link candidates with their issues from Wikidata"""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    
    # Query to get candidates and their positions on issues using multiple properties
    sparql.setQuery("""
    SELECT DISTINCT ?candidate ?candidateLabel ?issue ?issueLabel WHERE {
        ?candidate wdt:P31 wd:Q5;          # instance of human
             wdt:P106 wd:Q82955;     # occupation: politician
             wdt:P27 wd:Q30.         # country: United States

        {
            ?candidate wdt:P101 ?issue. # field of work
        } UNION {
            ?candidate wdt:P737 ?issue.
        } UNION {
            ?candidate wdt:P135 ?issue.
        } UNION {
            ?candidate wdt:P1142 ?issue.
        }

        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }

    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(f"SPARQL results count: {len(results['results']['bindings'])}")

    linked = 0
    for result in results["results"]["bindings"]:
        candidate_qid = result["candidate"]["value"].split("/")[-1]
        issue_qid = result["issue"]["value"].split("/")[-1]
        candidate_label = result.get("candidateLabel", {}).get("value", "Unknown")
        issue_label = result.get("issueLabel", {}).get("value", "Unknown")

        try:
            # Get or create the candidate
            candidate, _ = Candidate.objects.get_or_create(
                cqid=candidate_qid,
                defaults={
                    "label": candidate_label,
                }
            )

            # Get or create the issue
            issue, _ = Issue.objects.get_or_create(
                issue_qid=issue_qid,
                defaults={
                    "issue_label": issue_label
                }
            )
            
            # Create the link if it doesn't exist
            CandidateIssue.objects.get_or_create(
                candidate=candidate,
                issue=issue
            )
            linked += 1
            print(f"Linked {candidate_label} with {issue_label}")
        except Exception as e:
            print(f"Error processing {candidate_qid} - {issue_qid}: {str(e)}")
            continue

    return Response({"linked": linked})



@api_view(['GET'])
def get_candidate_issues_by_id(request, id):
    data = [
        {
            "candidate": ci.candidate.label,
            "issue": ci.issue.issue_label
        }
        for ci in CandidateIssue.objects.select_related('candidate', 'issue').filter(candidate__id=id)
    ]
    return Response(data)

@api_view(['GET'])
def get_similar_candidates(request, id):
    """Get similar candidates for a given candidate ID"""
    similar_candidates = CandidateSimilarity.objects.select_related('similar').filter(
        candidate_id=id
    ).order_by('-score')[:5]  # Get top 5 similar candidates
    
    data = [
        {
            "id": sim.similar.id,
            "label": sim.similar.label,
            "party_qid": sim.similar.party_qid,
            "ideology_qid": sim.similar.ideology_qid,
            "photo_url": sim.similar.photo_url,
            "similarity_score": sim.score
        }
        for sim in similar_candidates
    ]
    return Response(data)

@api_view(['POST'])
def calculate_similarity_scores(request):
    """Calculate and update similarity scores between candidates based on shared issues"""
    # Get all candidates
    candidates = Candidate.objects.all()
    
    # Clear existing similarity scores
    CandidateSimilarity.objects.all().delete()
    
    # For each pair of candidates
    for candidate1, candidate2 in combinations(candidates, 2):
        # Get their issues
        issues1 = set(CandidateIssue.objects.filter(candidate=candidate1).values_list('issue_id', flat=True))
        issues2 = set(CandidateIssue.objects.filter(candidate=candidate2).values_list('issue_id', flat=True))
        
        # Calculate Jaccard similarity
        if issues1 or issues2:  # Only calculate if at least one candidate has issues
            intersection = len(issues1.intersection(issues2))
            union = len(issues1.union(issues2))
            similarity_score = intersection / union if union > 0 else 0
            
            # Create similarity records in both directions
            CandidateSimilarity.objects.create(
                candidate=candidate1,
                similar=candidate2,
                score=similarity_score
            )
            CandidateSimilarity.objects.create(
                candidate=candidate2,
                similar=candidate1,
                score=similarity_score
            )
    
    return Response({"message": "Similarity scores updated successfully"})

def get_recent_bills(request):
    url = "https://api.congress.gov/v3/bill"
    headers = {
        "X-Api-Key": settings.CONGRESS_API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({'error': 'Failed to fetch bills'}, status=response.status_code)

class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'bill_id', 'sponsor__label']
    ordering_fields = ['introduced_date', 'last_action_date', 'congress']
    filterset_fields = ['congress', 'bill_type', 'status']

    @action(detail=True, methods=['get'])
    def votes(self, request, pk=None):
        """Get all votes for a specific bill"""
        bill = self.get_object()
        votes = Vote.objects.filter(bill=bill).select_related('candidate')
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['candidate__label', 'bill__title']
    ordering_fields = ['vote_date']
    filterset_fields = ['vote_position', 'chamber', 'congress']

@api_view(['POST'])
def update_candidates_with_bioguide_ids(request):
    """Update candidates with their Bioguide IDs from Wikidata"""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    
    # Query to get candidates and their Bioguide IDs
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
            print(f"Updated {candidate_label} with Bioguide ID: {bioguide_id}")
        except Candidate.DoesNotExist:
            print(f"Candidate {candidate_qid} not found in database")
        except Exception as e:
            print(f"Error updating {candidate_qid}: {str(e)}")

    return Response({"updated": updated})


@api_view(['POST'])
def fetch_bills_from_congress(request):
    """Fetch bills from Congress.gov API and store in database"""
    congress = request.data.get('congress', 118)  # 118 is current Congress
    bill_type = request.data.get('bill_type', 'hr')  # Default to House bills
    
    url = f"https://api.congress.gov/v3/bill"
    headers = {
        "X-Api-Key": settings.CONGRESS_API_KEY
    }
    
    params = {
        'congress': congress,
        'billType': bill_type,
        'format': 'json',
        'limit': 100  
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        created = updated = 0
        for bill_data in data.get('bills', []):
            try:
                # Extract bill information
                bill_id = bill_data.get('billId')
                title = bill_data.get('title', '')
                short_title = bill_data.get('shortTitle', {}).get('title', '')
                summary = bill_data.get('summary', '')
                
                # Extract sponsor information
                sponsor_data = bill_data.get('sponsors', [{}])[0] if bill_data.get('sponsors') else {}
                sponsor_bioguide_id = sponsor_data.get('bioguideId')
                
                # Extract dates
                introduced_date = bill_data.get('introducedDate')
                last_action_date = bill_data.get('latestAction', {}).get('actionDate')
                last_action_text = bill_data.get('latestAction', {}).get('text', '')
                
                # Parse bill ID components
                bill_parts = bill_id.split('-') if bill_id else []
                bill_type_code = bill_parts[0][:2] if bill_parts else ''
                bill_number = int(bill_parts[0][2:]) if len(bill_parts) > 0 and len(bill_parts[0]) > 2 else 0
                
                # Find sponsor candidate if bioguide_id exists
                sponsor_candidate = None
                if sponsor_bioguide_id:
                    try:
                        sponsor_candidate = Candidate.objects.get(bioguide_id=sponsor_bioguide_id)
                    except Candidate.DoesNotExist:
                        pass
                
                # Create or update bill
                bill, created_flag = Bill.objects.update_or_create(
                    bill_id=bill_id,
                    defaults={
                        'congress': congress,
                        'bill_type': bill_type_code,
                        'bill_number': bill_number,
                        'title': title,
                        'short_title': short_title,
                        'summary': summary,
                        'sponsor_bioguide_id': sponsor_bioguide_id,
                        'sponsor': sponsor_candidate,
                        'introduced_date': introduced_date,
                        'last_action_date': last_action_date,
                        'last_action_text': last_action_text,
                        'status': bill_data.get('latestAction', {}).get('actionBy', ''),
                        'congress_gov_url': bill_data.get('url', ''),
                    }
                )
                
                if created_flag:
                    created += 1
                else:
                    updated += 1
                    
            except Exception as e:
                print(f"Error processing bill {bill_id}: {str(e)}")
                continue
        
        return Response({
            "created": created,
            "updated": updated,
            "total_processed": created + updated
        })
        
    except requests.RequestException as e:
        return Response({"error": f"Failed to fetch bills: {str(e)}"}, status=500)


@api_view(['POST'])
def fetch_votes_from_congress(request):
    """Fetch votes from Congress.gov API and store in database"""
    congress = request.data.get('congress', 118)
    chamber = request.data.get('chamber', 'house') 
    
    url = f"https://api.congress.gov/v3/vote"
    headers = {
        "X-Api-Key": settings.CONGRESS_API_KEY
    }
    
    params = {
        'congress': congress,
        'chamber': chamber,
        'format': 'json',
        'limit': 50  
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        created = updated = 0
        for vote_data in data.get('votes', []):
            try:
                # Extract vote information
                roll_call = vote_data.get('roll')
                vote_date = vote_data.get('date')
                chamber_code = vote_data.get('chamber')
                session = vote_data.get('session')
                
                # Get bill information
                bill_data = vote_data.get('bill', {})
                bill_id = bill_data.get('billId')
                
                if not bill_id:
                    continue  # Skip votes not associated with bills
                
                # Get or create bill
                try:
                    bill = Bill.objects.get(bill_id=bill_id)
                except Bill.DoesNotExist:
                    # Create a minimal bill record if it doesn't exist
                    bill_parts = bill_id.split('-') if bill_id else []
                    bill_type_code = bill_parts[0][:2] if bill_parts else ''
                    bill_number = int(bill_parts[0][2:]) if len(bill_parts) > 0 and len(bill_parts[0]) > 2 else 0
                    
                    bill = Bill.objects.create(
                        bill_id=bill_id,
                        congress=congress,
                        bill_type=bill_type_code,
                        bill_number=bill_number,
                        title=f"Bill {bill_id}",
                    )
                
                # Process individual votes
                votes_data = vote_data.get('votes', {})
                for vote_position, voters in votes_data.items():
                    if vote_position in ['Yea', 'Nay', 'Present', 'Not Voting']:
                        for voter in voters:
                            bioguide_id = voter.get('bioguideId')
                            if bioguide_id:
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
                                    print(f"Candidate with Bioguide ID {bioguide_id} not found")
                                    continue
                    
            except Exception as e:
                print(f"Error processing vote {roll_call}: {str(e)}")
                continue
        
        return Response({
            "created": created,
            "updated": updated,
            "total_processed": created + updated
        })
        
    except requests.RequestException as e:
        return Response({"error": f"Failed to fetch votes: {str(e)}"}, status=500)


@api_view(['GET'])
def get_candidate_bills(request, candidate_id):
    """Get bills sponsored by a specific candidate"""
    try:
        candidate = Candidate.objects.get(id=candidate_id)
        bills = Bill.objects.filter(sponsor=candidate)
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)
    except Candidate.DoesNotExist:
        return Response({"error": "Candidate not found"}, status=404)


@api_view(['GET'])
def get_candidate_votes(request, candidate_id):
    """Get voting record for a specific candidate"""
    try:
        candidate = Candidate.objects.get(id=candidate_id)
        votes = Vote.objects.filter(candidate=candidate).select_related('bill').order_by('-vote_date')
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)
    except Candidate.DoesNotExist:
        return Response({"error": "Candidate not found"}, status=404)


@api_view(['GET'])
def get_bill_votes(request, bill_id):
    """Get all votes for a specific bill"""
    try:
        bill = Bill.objects.get(id=bill_id)
        votes = Vote.objects.filter(bill=bill).select_related('candidate').order_by('candidate__label')
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)
    except Bill.DoesNotExist:
        return Response({"error": "Bill not found"}, status=404)


def get_recent_bills(request):
    url = "https://api.congress.gov/v3/bill"
    headers = {
        "X-Api-Key": settings.CONGRESS_API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({'error': 'Failed to fetch bills'}, status=response.status_code)

