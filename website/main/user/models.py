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
		if len(post_data['password']) > 60:
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
		emailcheck = self.filter(email=post_data['email'])
		if emailcheck:
			errors['email'] = 'email already in use'
		#make sures passwords match in confirm password part of register
		if post_data['password'] != post_data['confirm_password']:
			errors['password'] = "Passwords must match"
		#returns any error in registration, if not will lead to success page
		return errors 
	#def authenticate(request):
	#	user = User.objects.get(email = request.POST['email'])
	#	if bcrypt.checkpw(request.POST['password'].encode(), user.pw_hash.encode)

# Users info
class User(models.Model):
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	email = models.CharField(max_length=45)
	address = models.CharField(max_length=255)
	zipcode = models.IntegerField()
	state = models.CharField(max_length=20)
	password = models.CharField(max_length=60)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# to call to UserManager to help validate info
	objects =UserManager()

#to validate reviews aren't empty
class ReviewManager(models.Manager):
	def reviewvalidate(self, reviewtext):
		errors = {}
		if len(reviewtext) < 2:
			errors['length'] = 'Reviews must be 2 or more characters'
		return errors
#for reviews left on site
class Review(models.Model):
	review = models.TextField()
	user = models.ForeignKey(User, related_name='review', on_delete=models.CASCADE)
	liked = models.ManyToManyField(User, related_name="liked_post")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ReviewManager()

#comments on reviews left, many to many
class Comment(models.Model):
	comment = models.CharField(max_length=255)
	user = models.ForeignKey(User, related_name='comment', on_delete=models.CASCADE)
	review = models.ForeignKey(Review, related_name='comment', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
#VALIDATING ITEMS LISTED
class ItemManager(models.Manager):
	def itemvalidate(self, post_data):
		errors = {}
		if len(post_data['itemname']) < 1:
			errors['itemname'] = "Item name must have a value"
		if len(post_data['price']) < 3:
			errors['price'] = "Price must be at least 3 characters"
		return errors
#items for sell
class Item(models.Model):
	itemname = models.CharField(max_length=45)
	description = models.CharField(max_length=255)
	price = models.DecimalField(decimal_places=2, max_digits=5)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)
	objects = ItemManager()

#For orders
class Order(models.Model):
	orders = models.CharField(max_length=45)
	totalprice = models.DecimalField(decimal_places=2, max_digits=6)
	user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)


