from django.shortcuts import render, redirect

from django.contrib.auth.models import User

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
	if request.user.is_authenticated:
		try:
			UserProfile.objects.get(user=request.user)
		except UserProfile.DoesNotExist:
			return redirect ('choose_type')
		if is_hunter(request):
			return redirect('hunter_home')
		else:
			return redirect('prospect_home')
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

def hunter_message(request):
	if request.user.is_authenticated:
		is_classified(request)
		pass

# Huntee Views
def prospect_home(request):
	if request.user.is_authenticated:
		is_classified(request)
		if not is_hunter(request):
			try:
				profile = ProspectProfile.objects.get(prospect=request.user)
			except ProspectProfile.DoesNotExist:
				return redirect('prospect_add_profile')
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
					return redirect('propsect_home')
			else:
				form = PropsectProfileForm()
			context = {
				'form': form
			}
			return render(request, 'main/prospect/add_profile.html', context)
	return redirect('landing')

def prospect_edit_profile(request):
	if request.user.is_authenticated:
		is_classified(request)
		pass

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
		ProspectCodeSnippet.objects.get(pk=snippet).delete()
		return redirect('prospect_home')
	return redirect('landing')

def prospect_add_education(request):
	if request.user.is_authenticated:
		is_classified(request)
		pass

def prospect_edit_education(request):
	if request.user.is_authenticated:
		is_classified(request)
		pass

def prospect_remove_education(request):
	if request.user.is_authenticated:
		is_classified(request)
		pass

def prospect_add_experience(request):
	if request.user.is_authenticated:
		is_classified(request)
		pass

def prospect_edit_experience(request):
	if request.user.is_authenticated:
		is_classified(request)
		pass

def prospect_remove_experience(request):
	if request.user.is_authenticated:
		is_classified(request)
		pass
