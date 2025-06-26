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
    bioguide_id = models.CharField(max_length=10, blank=True, null=True, unique=True)  # Congress.gov Bioguide ID
    last_updated = models.DateTimeField(auto_now=True)
    main_issues = models.TextField(blank=True, null=True)  # Comma-separated list of main issues
    start_date = models.DateField(blank=True, null=True)

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


class Bill(models.Model):
    bill_id = models.CharField(max_length=20, unique=True)  # e.g., "hr1234-118"
    congress = models.IntegerField()
    bill_type = models.CharField(max_length=10)  # hr, s, hjres, sjres, etc.
    bill_number = models.IntegerField()
    title = models.TextField()
    short_title = models.CharField(max_length=500, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    sponsor_bioguide_id = models.CharField(max_length=10, blank=True, null=True)
    sponsor = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True, blank=True, related_name='sponsored_bills')
    introduced_date = models.DateField(blank=True, null=True)
    last_action_date = models.DateField(blank=True, null=True)
    last_action_text = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    congress_gov_url = models.URLField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['congress']),
            models.Index(fields=['bill_type']),
            models.Index(fields=['sponsor_bioguide_id']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.bill_id}: {self.title[:50]}..."


class Vote(models.Model):
    VOTE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Present', 'Present'),
        ('Not Voting', 'Not Voting'),
    ]
    
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    vote_position = models.CharField(max_length=10, choices=VOTE_CHOICES)
    vote_date = models.DateField()
    chamber = models.CharField(max_length=10)  # house, senate
    roll_call = models.IntegerField()
    congress = models.IntegerField()
    session = models.IntegerField()
    
    class Meta:
        indexes = [
            models.Index(fields=['bill']),
            models.Index(fields=['candidate']),
            models.Index(fields=['vote_date']),
            models.Index(fields=['chamber']),
        ]
        unique_together = ['bill', 'candidate', 'roll_call']

    def __str__(self):
        return f"{self.candidate.label} voted {self.vote_position} on {self.bill.bill_id}"
