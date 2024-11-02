from django import forms


class SearchForm(forms.Form):
    start_date = forms.DateField(label="Start Date")
    end_date = forms.DateField(label="End Date")

    radius = forms.IntegerField(min_value=1, max_value=500)
    anywhere = forms.BooleanField(required=False)

    def clean(self):
        data = super(SearchForm, self).clean()
        data = self.cleaned_data

        if data["end_date"] < data["start_date"]:
            raise forms.ValidationError("End Date before Start Date.")
