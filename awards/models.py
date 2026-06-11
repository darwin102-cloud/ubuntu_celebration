from django.db import models
from django.utils import timezone
class AwardSection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    section = models.ForeignKey(
        AwardSection,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Nominee(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='nominees'
    )

    full_name = models.CharField(max_length=255)

    photo = models.ImageField(
        upload_to='nominees/',
        blank=True,
        null=True
    )

    bio = models.TextField()

    organization = models.CharField(
        max_length=255,
        blank=True
    )

    votes = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name


class Vote(models.Model):
    nominee = models.ForeignKey(
        Nominee,
        on_delete=models.CASCADE,
        related_name='votes_received'
    )

    voter_name = models.CharField(
        max_length=255
    )

    phone_number = models.CharField(
        max_length=20
    )

    votes = models.PositiveIntegerField(
        default=1
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    transaction_code = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.voter_name} - {self.nominee.full_name}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)

    event_date = models.DateField()

    voting_start = models.DateTimeField()
    voting_end = models.DateTimeField()

    motto = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def voting_open(self):
        now = timezone.now()
        return self.voting_start <= now <= self.voting_end

class SiteSettings(models.Model):
    event_name = models.CharField(max_length=255)

    venue = models.CharField(max_length=255)

    event_date = models.DateField()

    voting_start = models.DateTimeField()

    voting_end = models.DateTimeField()

    contact_phone = models.CharField(max_length=20)

    contact_email = models.EmailField()

    facebook = models.CharField(max_length=255)

    tiktok = models.CharField(max_length=255)

    logo = models.ImageField(upload_to='settings/')

class Nomination(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    nominee_name = models.CharField(
        max_length=255
    )

    photo = models.ImageField(
        upload_to='nominations/',
        blank=True,
        null=True
    )

    organization = models.CharField(
        max_length=255,
        blank=True
    )

    bio = models.TextField()

    nominator_name = models.CharField(
        max_length=255
    )

    nominator_phone = models.CharField(
        max_length=20
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    approved = models.BooleanField(
        default=False
    )

    processed = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.nominee_name