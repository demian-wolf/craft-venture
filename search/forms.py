from django import forms

from .models import UserSearch


class SearchForm(forms.ModelForm):
    class Meta:
        model = UserSearch
        
        fields = ["starts_at", "ends_at", "radius"]
        
        widgets = {
            "starts_at": forms.DateInput(attrs={"type": "date"}),
            "ends_at": forms.DateInput(attrs={"type": "date"}),
        }
