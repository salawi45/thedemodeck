from django.core.management.base import BaseCommand
from candidates.models import Candidate
import requests
from datetime import datetime


class Command(BaseCommand):
    help = "Import current U.S. Senators and Representatives from Wikidata"

    def handle(self, *args, **kwargs):
        url = "https://query.wikidata.org/sparql"
        query = """
        SELECT
          ?member ?memberLabel
          ?positionLabel
          ?startDate
          ?ideology
          ?ideologyLabel
          ?bioguideId
          ?image
          (GROUP_CONCAT(DISTINCT ?issueLabel; separator=", ") AS ?mainIssues)
        WHERE {
          VALUES ?position {
            wd:Q13218630   # United States Senator
            wd:Q15842528   # Member of the United States House of Representatives
          }
          ?member p:P39 ?posStmt.
          ?posStmt ps:P39 ?position.
          OPTIONAL { ?posStmt pq:P580 ?startDate. }
          FILTER NOT EXISTS { ?posStmt pq:P582 ?endDate. }
          OPTIONAL { ?member wdt:P1142 ?ideology. }
          OPTIONAL { ?member wdt:P921 ?issue. }
          OPTIONAL { ?member wdt:P1157 ?bioguideId. }
          OPTIONAL { ?member wdt:P18 ?image. }
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        GROUP BY
          ?member ?memberLabel
          ?positionLabel
          ?startDate
          ?ideology
          ?ideologyLabel
          ?bioguideId
          ?image
        ORDER BY
          ?positionLabel
          DESC(?startDate)
        """

        headers = {"Accept": "application/sparql-results+json"}

        try:
            response = requests.get(url, params={'query': query}, headers=headers)
            data = response.json()
        except requests.exceptions.ReadTimeout:
            self.stdout.write(self.style.ERROR("❌ Request to Wikidata timed out. Try again later."))
            return

        count = 0
        for result in data['results']['bindings']:
            cqid = result.get('member', {}).get('value', '').split('/')[-1]
            label = result.get('memberLabel', {}).get('value', '')
            position = result.get('positionLabel', {}).get('value', '')
            ideology_qid = result.get('ideology', {}).get('value', '').split('/')[-1] if result.get('ideology', {}).get('value', '') else None
            main_issues = result.get('mainIssues', {}).get('value', '')
            bioguide_id = result.get('bioguideId', {}).get('value', None)
            photo_url = result.get('image', {}).get('value', None)

            start_date_raw = result.get('startDate', {}).get('value', '')
            try:
                start_date = datetime.strptime(start_date_raw, "%Y-%m-%d").date() if start_date_raw else None
            except:
                start_date = None

            Candidate.objects.update_or_create(
                cqid=cqid,
                defaults={
                    'label': label,
                    'position': position,
                    'ideology_qid': ideology_qid,
                    'main_issues': main_issues,
                    'bioguide_id': bioguide_id,
                    'photo_url': photo_url,
                    'start_date': start_date
                }
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {count} candidates"))
