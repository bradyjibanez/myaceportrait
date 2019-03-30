from django.urls import path, include
from . import views

urlpatterns = [
	# Generic Views
	path('', views.landing, name='landing'),
	path('accounts/signup/', views.signup, name='signup'),
	path('accounts/type/', views.choose_type, name='choose_type'),
	# Hunter Views
	path('h/home', views.hunter_home, name='hunter_home'),
	path('h/prospect/<int:prospect>', views.hunter_view, name='hunter_view'),
	path('h/prospect/<int:prospect>/message', views.hunter_message, name='hunter_message'),
	# Huntee views
	path('p/home', views.prospect_home, name='prospect_home')
]