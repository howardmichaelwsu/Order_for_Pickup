from django.db import models
from datetime import datetime
import bcrypt, re

class UserManager(models.Manager):
	def basic_validation(self, post_data):
		#error message, starts empty then validation messages will appear.
		errors = {}
		#email format validation
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		#setting length minimum for password, first & last name, and zipcode and error message that pops up directing user
		if len(post_data['password']) < 8:
			errors['password'] = "Your password needs to be at least 8 characters"
		if len(post_data['password']) > 46:
			errors['password'] = "Password can not be over 45 characters"
		if len(post_data['first_name']) < 2:
			errors['first_name'] = "First name must be 2 characters or more"
		if len(post_data['last_name']) < 2:
			errors['last_name'] ="Last name must be 2 characters or more"
		if len(post_data['zipcode']) != 5:
			errors['zipcode'] = "Zipcode must be 5 digits"
		#validating email
		if not EMAIL_REGEX.match(post_data['email']):
			errors['email'] = "Email must be valid"
		#make sures passwords match in confirm password part of register
		if post_data['password'] != post_data['confirm_password']:
			errors['password'] = "Passwords must match"
		#returns any error in registration, if not will lead to success page
		return errors 
	def authenticate(self, email, password):
		users = self.filter(email=email)
		if not users:
			return False
		user = users[0]
		return bcrypt.checkpw(password.encode(), user.password.encode())

# Users info
class User(models.Model):
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	email = models.CharField(max_length=45)
	address = models.CharField(max_length=255)
	zipcode = models.IntegerField()
	state = models.CharField(max_length=20)
	password = models.CharField(max_length=45)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# to call to UserManager to help validate info
	objects =UserManager()

