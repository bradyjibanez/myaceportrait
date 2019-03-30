from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from main.models import UserProfile, ProspectProfile, ProspectCodeSnippet, ProspectEducation, ProspectExperience

class RegistrationForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False)
	last_name = forms.CharField(max_length=30, required=False)
	email = forms.EmailField(max_length=254, help_text='Required')

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'col-8'

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['user_type']
		exclude = ['user']

class ProspectProfileForm(forms.ModelForm):
	bio = forms.CharField(max_length=10000, widget=forms.Textarea)
	class Meta:
		model = ProspectProfile
		fields = ['github', 'bio']
		exclude = ['prospect']

class ProspectCodeSnippetForm(forms.ModelForm):
	snippet_code = forms.CharField(max_length=10000, widget=forms.Textarea)
	class Meta:
		model = ProspectCodeSnippet
		fields = ['snippet_name', 'snippet_code']
		exclude = ['prospect', 'date_created']

class ProspectEducationForm(forms.ModelForm):
	class Meta:
		model = ProspectEducation
		fields = ['institution', 'edu_type', 'edu_subject', 'start_date', 'end_date']
		exclude = ['prospect', 'date_created']

class ProspectExperienceForm(forms.ModelForm):
	class Meta:
		model = ProspectExperience
		fields = ['name', 'position', 'work_type', 'location', 'start_date', 'end_date']
		exclude = ['prospect', 'date_created']