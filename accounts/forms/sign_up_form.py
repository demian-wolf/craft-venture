from django import forms


class SignUpForm(forms.Form):
    email = forms.EmailField(label='Email',
                             required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control pl-4',
                                                            'id': 'email',
                                                            'placeholder': 'Email'}))
    password = forms.CharField(label='Password', required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control pl-5',
                                                                 'id': 'password',
                                                                 'placeholder': 'Password'}))
    confirm_password = forms.CharField(required=True, label='Confirm Password',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control pl-5',
                                                                         'id': 'confirm-password',
                                                                         'placeholder': 'Confirm Password'}))

