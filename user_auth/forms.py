from django import forms
from django.contrib.auth.forms import UserCreationForm

from user_auth.models import User


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistration(forms.ModelForm):
    password = forms.CharField(label='Password', min_length=8, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', required=True, widget=forms.PasswordInput)
    date_of_birth = forms.CharField(label='Date Of Birth', required=True,
                                    widget=forms.TextInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('M', "Male"), ('F', 'Female')], widget=forms.RadioSelect())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'gender', 'password')

    '''
        def clean_password2(self):
        cd = self.cleaned_data
        print(cd)
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    '''

    def clean_password2(self):
        if not self.cleaned_data.get('password'):
            raise forms.ValidationError('Invalid Password')
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise forms.ValidationError('Password does not match the confirm password.')
        return self.cleaned_data
