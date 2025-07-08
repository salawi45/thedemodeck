from django.core.management.base import BaseCommand
from candidates.models import Candidate

class Command(BaseCommand):
    help = 'Force all candidates to have chamber values for filter testing.'

    def handle(self, *args, **options):
        # Set all candidates with any non-null, non-empty chamber containing 'house' to 'house'
        house_fixed = Candidate.objects.filter(chamber__icontains='house').update(chamber='house')
        # Set all other candidates with any non-null, non-empty chamber to 'senate'
        senate_fixed = Candidate.objects.exclude(chamber__icontains='house').exclude(chamber__isnull=True).exclude(chamber='').update(chamber='senate')
        # Forcibly set at least one candidate to 'senate' and one to 'house' for testing
        first = Candidate.objects.first()
        if first:
            first.chamber = 'senate'
            first.save()
        last = Candidate.objects.last()
        if last:
            last.chamber = 'house'
            last.save()
        self.stdout.write(self.style.SUCCESS(f'Updated {house_fixed} candidates to chamber="house"'))
        self.stdout.write(self.style.SUCCESS(f'Updated {senate_fixed} candidates to chamber="senate"'))
        self.stdout.write(self.style.SUCCESS('Ensured at least one candidate for each chamber.')) 