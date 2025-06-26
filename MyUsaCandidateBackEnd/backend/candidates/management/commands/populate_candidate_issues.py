from django.core.management.base import BaseCommand
from candidates.models import Candidate, Issue, CandidateIssue

class Command(BaseCommand):
    help = "Link candidates to issues from their 'main_issues' field"

    def handle(self, *args, **kwargs):
        count_created_links = 0
        count_created_issues = 0

        for candidate in Candidate.objects.exclude(main_issues__isnull=True).exclude(main_issues=""):
            issues_raw = [i.strip() for i in candidate.main_issues.split(",") if i.strip()]
            for issue_label in issues_raw:
                # Create or get the Issue
                issue, created = Issue.objects.get_or_create(
                    issue_label=issue_label,
                    defaults={'issue_qid': f"ISSUE_{issue_label.replace(' ', '_')[:15]}"}
                )
                if created:
                    count_created_issues += 1

                # Link to Candidate if not already linked
                if not CandidateIssue.objects.filter(candidate=candidate, issue=issue).exists():
                    CandidateIssue.objects.create(candidate=candidate, issue=issue)
                    count_created_links += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Linked {count_created_links} issues to candidates, created {count_created_issues} new issues."
        ))
