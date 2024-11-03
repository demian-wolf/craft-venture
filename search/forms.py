from django import forms

from .models import UserSearch, UserSearchStage


class SearchForm(forms.ModelForm):
    class Meta:
        model = UserSearch
        
        fields = ["starts_at", "ends_at", "radius", "lat", "lng"]
        
        widgets = {
            "starts_at": forms.DateInput(attrs={"type": "date"}),
            "ends_at": forms.DateInput(attrs={"type": "date"}),
        }


class UserSearchStageForm(forms.ModelForm):
    class Meta:
        model = UserSearchStage

        fields = ["is_accepted"]
