from django.db import models

class Candidate(models.Model):
    cqid = models.CharField(max_length=20, unique=True)  # Wikidata QID
    label = models.CharField(max_length=255)
    description = models.CharField(max_length=512, blank=True, null=True)  # e.g. "American politician"
    position = models.CharField(max_length=255, blank=True, null=True)     # e.g. "Senator"
    party_qid = models.CharField(max_length=20, blank=True, null=True)     # party affiliation QID
    ideology_qid = models.CharField(max_length=200, blank=True, null=True)  # ideology QID
    dob = models.DateField(blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label


class Issue(models.Model):
    issue_qid = models.CharField(max_length=20, unique=True)
    issue_label = models.CharField(max_length=255)

    def __str__(self):
        return self.issue_label


class CandidateIssue(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['issue']),
        ]

    def __str__(self):
        return f"{self.candidate.label} - {self.issue.issue_label}"


class CandidateSimilarity(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='similarities')
    similar = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='similar_to')
    score = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=['candidate']),
        ]

    def __str__(self):
        return f"{self.candidate.label} ~ {self.similar.label}: {self.score}"
