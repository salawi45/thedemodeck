from django.core.management.base import BaseCommand
from candidates.models import Candidate
from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import date
import re

def parse_date(val):
    if val and re.match(r'^\\d{4}-\\d{2}-\\d{2}', val):
        return val[:10]
    return None

class Command(BaseCommand):
    help = 'Import currently active U.S. Senators and House members who can participate in votes.'

    def handle(self, *args, **kwargs):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery("""
        SELECT DISTINCT ?item ?itemLabel ?positionLabel ?party ?partyLabel ?ideology ?ideologyLabel
                        ?dob ?description ?image ?bioguide ?start WHERE {
          ?item p:P39 ?statement.
          ?statement ps:P39 ?position.
          FILTER(?position IN (wd:Q13218630, wd:Q16707842))  # Senate or House

          OPTIONAL { ?statement pq:P580 ?start. }
          OPTIONAL { ?statement pq:P582 ?end. }
          FILTER (!BOUND(?end) || ?end > NOW())  # Still active

          OPTIONAL { ?item wdt:P102 ?party. }
          OPTIONAL { ?item wdt:P1142 ?ideology. }
          OPTIONAL { ?item wdt:P569 ?dob. }
          OPTIONAL { ?item schema:description ?description. FILTER(LANG(?description)="en") }
          OPTIONAL { ?item wdt:P18 ?image. }
          OPTIONAL { ?item wdt:P1157 ?bioguide. }

          FILTER(BOUND(?bioguide))  # Must have bioguide ID to be trackable in votes

          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        """)
        sparql.setReturnFormat(JSON)

        try:
            results = sparql.query().convert()["results"]["bindings"]
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"SPARQL query failed: {e}"))
            return

        created = updated = 0

        for result in results:
            qid = result["item"]["value"].split("/")[-1]
            label = result.get("itemLabel", {}).get("value", "")
            position_label = result.get("positionLabel", {}).get("value", "")
            party_qid = result.get("party", {}).get("value", "").split("/")[-1] if "party" in result else None
            ideology_qid = result.get("ideology", {}).get("value", "").split("/")[-1] if "ideology" in result else None
            dob = parse_date(result.get("dob", {}).get("value"))
            description = result.get("description", {}).get("value", "")
            photo_url = result.get("image", {}).get("value", "")
            bioguide_id = result.get("bioguide", {}).get("value", None)
            start_date = parse_date(result.get("start", {}).get("value"))

            if "Senate" in position_label:
                chamber = "senate"
                position = "Senator"
            elif "House" in position_label:
                chamber = "house"
                position = "Member of the House of Representatives"
            else:
                continue  # Skip if unknown

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
                    "main_issues": None,
                    "start_date": start_date,
                    "chamber": chamber,
                    "position": position,
                    "last_updated": date.today(),
                }
            )

            if created_flag:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Congress import complete. Created: {created}, Updated: {updated}."
        ))
