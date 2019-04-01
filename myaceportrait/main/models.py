from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	TYPE = (
		('HUNTER', 'Hunter'),
		('PROSPECT', 'Prospect')
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_type = models.CharField(max_length=250, choices=TYPE)

	def __str__(self):
		return "%s (%s)" % (self.user.username, self.user_type)

class ProspectProfile(models.Model):
	prospect = models.OneToOneField(User, on_delete=models.CASCADE)
	github = models.CharField(max_length=100, blank=True, null=True)
	bio = models.CharField(max_length=10000, blank=True, null=True)

	def __str__(self):
		return self.prospect.username

class ProspectCodeSnippet(models.Model):
	prospect = models.ForeignKey(User, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	snippet_name = models.CharField(max_length=100)
	snippet_code = models.CharField(max_length=10000)

	def __str__(self):
		return "%s: %s" % (self.prospect.username, self.snippet_name)

class ProspectEducation(models.Model):
	TYPE = (
		('C', 'Certificate'),
		('D', 'Diploma'),
		('B', 'Bachelors'),
		('M', 'Masters'),
		('P', 'PhD')
	)

	prospect = models.ForeignKey(User, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	institution = models.CharField(max_length=100)
	edu_type = models.CharField(max_length=100, choices=TYPE)
	edu_subject = models.CharField(max_length=100)
	start_date = models.DateField()
	end_date = models.DateField()

	def __str__(self):
		return "%s, (%s, %s in %s)" % (self.prospect.username, self.institution, self.edu_type, self.edu_subject)

class ProspectExperience(models.Model):
	TYPE = (
		('W', 'Work'),
		('I', 'Internship'),
		('V', 'Volunteer')
	)

	prospect = models.ForeignKey(User, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	position = models.CharField(max_length=100)
	work_type = models.CharField(max_length=20, choices=TYPE)
	name = models.CharField(max_length=250)
	location = models.CharField(max_length=250)
	start_date = models.DateField()
	end_date = models.DateField()

	def __str__(self):
		return "%s, (%s in %s, %s)" % (self.prospect.username, self.name, self.location, self.work_type)