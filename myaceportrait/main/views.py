from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from main.models import *
from main.forms import *

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
		if is_hunter(request):
			return redirect('hunter_home')
		else:
			return redirect('huntee_home')
	return render(request, 'main/landing.html')

# Hunter Views
def hunter_home(request):
	if request.user.is_authenticated:
		if is_hunter(request):
			prospect = UserProfile.objects.filter(user_type__iexact="PROSPECT").order_by('user.username')
			context = {
				'prospects': prospects
			}
			return render(request, 'main/hunter/home.html', context)
	return redirect('landing')

def hunter_view_all(request):
	pass

def hunter_view(request, prospect=None):
	pass

def hunter_message(request):
	pass

# Huntee Views
def prospect_home(request):
	if request.user.is_authenticated:
		if not is_hunter(request):
			profile = HunteeProfile.objects.get(prospect=request.user)
			snippets = HunteeCodeSnippet.objects.filter(prospect=request.user).order_by('-date_created')
			education = HunteeEducation.objects.filter(prospect=request.user).order_by('-date_created')
			experience = HunteeExperience.objects.filter(prospect=request.user).order_by('-date_created')
			context = {
				'profile': profile,
				'snippets': snippets,
				'education': education,
				'experience': experience
			}
			return render(request, 'main/prospect/home/html', context)
	return redirect('landing')

def prospect_edit_profile(request):
	pass

def prospect_add_snippet(request):
	if request.user.is_authenticated:
		if not is_hunter(request):
			if request.method == 'POST':
				form = ProspectCodeSnippetForm(request.data)
				form.prospect = request.user
				if form.is_valid():
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
		if not is_hunter(request):
			snippet = ProspectCodeSnippet.objects.get(pk=snippet)
			if request.method == 'POST':
				form = ProspectCodeSnippetForm(request.data, instance=snippet)
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
		ProspectCodeSnippet.objects.get(pk=snippet).delete()
		return redirect('prospect_home')
	return redirect('landing')

def prospect_add_education(request):
	pass

def prospect_edit_education(request):
	pass

def prospect_remove_education(request):
	pass

def prospect_add_experience(request):
	pass

def prospect_edit_experience(request):
	pass

def prospect_remove_experience(request):
	pass