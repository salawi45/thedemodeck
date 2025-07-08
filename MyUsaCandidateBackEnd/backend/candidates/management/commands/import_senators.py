from django.core.management.base import BaseCommand
from candidates.models import Candidate
from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import date

class Command(BaseCommand):
    help = 'Import all currently active U.S. Senators from Wikidata, populating all available fields.'

    def handle(self, *args, **options):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery('''
        SELECT ?item ?itemLabel ?party ?partyLabel ?ideology ?ideologyLabel ?dob ?description ?image ?bioguide ?start WHERE {
          ?item p:P39 ?statement.
          ?statement ps:P39 wd:Q13218630;  # position held: member of the United States Senate
                    pq:P580 ?start.
          FILTER NOT EXISTS { ?statement pq:P582 ?end. FILTER(?end < NOW()) }
          OPTIONAL { ?item wdt:P102 ?party. }
          OPTIONAL { ?item wdt:P1142 ?ideology. }
          OPTIONAL { ?item wdt:P569 ?dob. }
          OPTIONAL { ?item schema:description ?description. FILTER(LANG(?description)="en") }
          OPTIONAL { ?item wdt:P18 ?image. }
          OPTIONAL { ?item wdt:P1157 ?bioguide. }
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        ''')
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print("Wikidata results:", len(results["results"]["bindings"]))

        created = updated = 0
        for result in results["results"]["bindings"]:
            qid = result["item"]["value"].split("/")[-1]
            label = result["itemLabel"]["value"]
            party_qid = result.get("party", {}).get("value", "").split("/")[-1] if "party" in result else None
            ideology_qid = result.get("ideology", {}).get("value", "").split("/")[-1] if "ideology" in result else None
            dob_raw = result.get("dob", {}).get("value", None)
            dob = dob_raw[:10] if dob_raw else None
            photo_url = result.get("image", {}).get("value", "")
            description = result.get("description", {}).get("value", "")
            bioguide_id = result.get("bioguide", {}).get("value", None)
            start_raw = result.get("start", {}).get("value", None)
            start_date = start_raw[:10] if start_raw else None

            candidate, created_flag = Candidate.objects.update_or_create(
                cqid=qid,
                defaults={
                    "label": label,
                    "party_qid": party_qid,
                    "ideology_qid": ideology_qid,
                    "dob": dob,
                    "photo_url": photo_url,
                    "description": description,
                    "bioguide_id": bioguide_id,
                    "main_issues": None,  # Not available from Wikidata in this query
                    "start_date": start_date,
                    "chamber": "senate",
                    "position": "Senator",
                    "last_updated": date.today(),
                }
            )
            if created_flag:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} and updated {updated} senators."))