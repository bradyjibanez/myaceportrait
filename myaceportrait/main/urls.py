from django.urls import path, include
from . import views

urlpatterns = [
	# Generic Views
	path('', views.landing, name='landing'),
	# Hunter Views
	path('h/home', views.hunter_home, name='hunter_home'),
	path('h/propsects', views.hunter_view_all, name='hunter_view_all'),
	path('h/prospect/<int:prospect>', views.hunter_view, name='hunter_view'),
	path('h/prospect/<int:prospect>/message', views.hunter_message, name='hunter_message'),
	# Huntee views
	path('p/home', views.prospect_home, name='prospect_home')
]