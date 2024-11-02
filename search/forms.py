from django import forms

from .models import UserSearch, SearchFeedback


class SearchForm(forms.ModelForm):
    class Meta:
        model = UserSearch
        
        fields = ["start_date", "end_date", "radius"]
        
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
