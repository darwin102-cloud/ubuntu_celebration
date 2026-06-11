from django import forms
from .models import Vote
from .models import Nomination

class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = [
            'voter_name',
            'phone_number',
            'votes'
        ]

class NominationForm(forms.ModelForm):

    class Meta:
        model = Nomination

        fields = [
            'category',
            'nominee_name',
            'photo',
            'organization',
            'bio',
            'nominator_name',
            'nominator_phone'
        ]