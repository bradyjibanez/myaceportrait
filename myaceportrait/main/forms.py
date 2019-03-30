from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from main.models import UserProfile, ProspectProfile, ProspectCodeSnippet, ProspectEducation, ProspectExperience

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
		fields = ['name', 'work_type', 'location', 'start_date', 'end_date']
		exclude = ['prospect', 'date_created']