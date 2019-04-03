from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.core.mail import send_mail

from main.models import *
from main.forms import *

def is_classified(request):
	if not UserProfile.objects.get(user=request.user):
		return redirect('choose_type')

def is_hunter(request):
	profile = UserProfile.objects.get(user=request.user)
	user_type = profile.user_type
	if user_type == 'HUNTER':
		return True
	else:
		return False

# Generic Views
def landing(request):
	#if request.user.is_authenticated:
	try:
		print("SO CLOSE")
		UserProfile.objects.get(user=request.user)
	except UserProfile.DoesNotExist:
		return redirect ('choose_type')
	if is_hunter(request):
		return redirect('hunter_home')
	else:
		return redirect('prospect_home')
#	else:
	return render(request, 'main/landing.html')

def choose_type(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = UserProfileForm(request.POST)
			if form.is_valid():
				form = form.save(commit=False)
				form.user = request.user
				form.save()
				return redirect('landing')
		else:
			form = UserProfileForm()
		context = {
			'form': form
		}
		return render(request, 'registration/choose_type.html', context)
	return redirect('landing')

def signup(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/accounts/login')
	else:
		form = RegistrationForm()
	context = {
		'form': form
	}
	return render(request, 'registration/signup.html', context)


# Hunter Views
def hunter_home(request):
	if request.user.is_authenticated:
		is_classified(request)
		if is_hunter(request):
			prospects = UserProfile.objects.filter(user_type="PROSPECT")
			prospect_profiles = ProspectProfile.objects.all()
			context = {
				'prospects': prospects,
				'prospect_profiles': prospect_profiles
			}
			return render(request, 'main/hunter/home.html', context)
	return redirect('landing')

def hunter_view(request, prospect=None):
	if request.user.is_authenticated:
		is_classified(request)
		if is_hunter(request):
			user = User.objects.get(pk=prospect)
			prospect = ProspectProfile.objects.get(prospect=user)
			education = ProspectEducation.objects.filter(prospect=user)
			experience = ProspectExperience.objects.filter(prospect=user)
			snippets = ProspectCodeSnippet.objects.filter(prospect=user)
			context = {
				'prospect': prospect,
				'education': education,
				'experience': experience,
				'snippets': snippets
			}
			return render(request, 'main/hunter/prospect.html', context)
	return redirect('landing')

def hunter_message(request, prospect=None):
	if request.user.is_authenticated:
		is_classified(request)
		if is_hunter(request):
			if request.method == "POST":
				form = ContactForm(request.POST)
				if form.is_valid():
					data = form.cleaned_data
					
					subject = 'myACEportrait - Message from '+str(request.user.username)
					message = data['message']
					from_email = str(request.user.email)
					prospect = User.objects.get(pk=prospect)
					recipients = [prospect.email]
					
					send_mail(subject, message, from_email, recipients, fail_silently=False)
					return redirect('hunter_home')
			else:
				form = ContactForm()
			context = {
				'form': form
			}
			return render(request, 'main/hunter/send_mail.html', context)

# Prospect Views
def prospect_home(request):
	if request.user.is_authenticated:
		is_classified(request)
		if not is_hunter(request):
			try:
				profile = ProspectProfile.objects.get(prospect=request.user)
			except ProspectProfile.DoesNotExist:
				return redirect('/p/profile/create')
			snippets = ProspectCodeSnippet.objects.filter(prospect=request.user).order_by('-date_created')
			education = ProspectEducation.objects.filter(prospect=request.user).order_by('-date_created')
			experience = ProspectExperience.objects.filter(prospect=request.user).order_by('-date_created')
			context = {
				'profile': profile,
				'snippets': snippets,
				'education': education,
				'experience': experience
			}
			return render(request, 'main/prospect/home.html', context)
	return redirect('landing')

def prospect_add_profile(request):
	if request.user.is_authenticated:
		is_classified(request)
		if not is_hunter(request):
			if request.method == 'POST':
				form = ProspectProfileForm(request.POST)
				if form.is_valid():
					form = form.save(commit=False)
					form.prospect = request.user
					form.save()
					return redirect('prospect_home')
			else:
				form = ProspectProfileForm()
			context = {
				'form': form
			}
			return render(request, 'main/prospect/add_profile.html', context)
	return redirect('landing')

def prospect_edit_profile(request):
	if request.user.is_authenticated:
		is_classified(request)
		if not is_hunter(request):
			profile = ProspectProfile.objects.get(prospect=request.user)
			if request.method == 'POST':
				form = ProspectProfileForm(request.POST, instance=profile)
				if form.is_valid():
					form.save()
					return redirect('prospect_home')
			else:
				form = ProspectProfileForm(instance=profile)
			context =  {
				'form': form
			}
			return render(request, 'main/prospect/add_profile.html', context)

def prospect_add_snippet(request):
	if request.user.is_authenticated:
		is_classified(request)
		if not is_hunter(request):
			if request.method == 'POST':
				form = ProspectCodeSnippetForm(request.POST)
				if form.is_valid():
					form = form.save(commit=False)
					form.prospect = request.user
					form.save()
					return redirect('prospect_home')
			else:
				form = ProspectCodeSnippetForm()
			context = {
				'form': form
			}
			return render(request, 'main/prospect/add_snippet.html', context)
	return redirect('landing')

def prospect_edit_snippet(request, snippet=None):
	if request.user.is_authenticated:
		is_classified(request)
		if not is_hunter(request):
			snippet = ProspectCodeSnippet.objects.get(pk=snippet)
			if snippet.prospect == request.user:
				if request.method == 'POST':
					form = ProspectCodeSnippetForm(request.POST, instance=snippet)
					if form.is_valid():
						form.save()
						return redirect('prospect_home')
				else:
					form = ProspectCodeSnippetForm(instance=snippet)
				context = {
					'form': form
				}
				return render(request, 'main/prospect/add_snippet.html', context)
	return redirect('landing')

def prospect_remove_snippet(request, snippet=None):
	if request.user.is_authenticated:
		is_classified(request)
		snippet = ProspectCodeSnippet.objects.get(pk=snippet)
		if snippet.prospect == request.user:
			ProspectCodeSnippet.objects.get(pk=snippet).delete()
		return redirect('prospect_home')
	return redirect('landing')

def prospect_add_education(request):
	if request.user.is_authenticated:
		is_classified(request)
		if not is_hunter(request):
			if request.method == 'POST':
				form = ProspectEducationForm(request.POST)
				if form.is_valid():
					form = form.save(commit=False)
					form.prospect = request.user
					form.save()
					return redirect('prospect_home')
			else:
				form = ProspectEducationForm()
			context = {
				'form': form
			}
			return render(request, 'main/prospect/add_education.html', context)
	return redirect('landing')

def prospect_edit_education(request, education=None):
	if request.user.is_authenticated:
		is_classified(request)
		if not is_hunter(request):
			education = ProspectEducation.objects.get(pk=education)
			if education.prospect == request.user:
				if request.method == 'POST':
					form = ProspectEducationForm(request.POST, instance=education)
					if form.is_valid():
						form = form.save(commit=False)
						form.prospect = request.user
						form.save()
						return redirect('prospect_home')
				else:
					form = ProspectEducationForm(instance=education)
				context = {
					'form': form
				}
				return render(request, 'main/prospect/add_education.html', context)
	return redirect('landing')

def prospect_remove_education(request, education=None):
	if request.user.is_authenticated:
		is_classified(request)
		education = ProspectEducation.objects.get(pk=education)
		if education.prospect == request.user:
			ProspectEducation.objects.get(pk=education).delete()
		return redirect('prospect_home')
	return redirect('landing')

def prospect_add_experience(request):
	if request.user.is_authenticated:
		is_classified(request)
		if not is_hunter(request):
			if request.method == 'POST':
				form = ProspectExperienceForm(request.POST)
				if form.is_valid():
					form = form.save(commit=False)
					form.prospect = request.user
					form.save()
					return redirect('prospect_home')
			else:
				form = ProspectExperienceForm()
			context = {
				'form': form
			}
			return render(request, 'main/prospect/add_experience.html', context)
	return redirect('landing')

def prospect_edit_experience(request, experience=None):
	if request.user.is_authenticated:
		is_classified(request)
		if not is_hunter(request):
			experience = ProspectEducation.objects.get(pk=experience)
			if education.prospect == request.user:
				if request.method == 'POST':
					form = ProspectExperienceForm(request.POST, instance=experience)
					if form.is_valid():
						form = form.save(commit=False)
						form.prospect = request.user
						form.save()
						return redirect('prospect_home')
				else:
					form = ProspectExperienceForm(instance=experience)
				context = {
					'form': form
				}
				return render(request, 'main/prospect/add_experience.html', context)
	return redirect('landing')

def prospect_remove_experience(request, experience=None):
	if request.user.is_authenticated:
		is_classified(request)
		experience = ProspectExperience.objects.get(pk=education)
		if experience.prospect == request.user:
			ProspectExperience.objects.get(pk=education).delete()
		return redirect('prospect_home')
	return redirect('landing')
