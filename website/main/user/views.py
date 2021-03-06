from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.db.models import Sum
import requests
poke_api = "https://pokeapi.co/api/v2/pokemon"
google_maps_api = "https://www.google.com/maps/embed/v1/place?key=AIzaSyBe0y2GxJYzJ20hfHtoos14qa-sidumRIk&q=Eiffel+Tower,Paris+France"

#home page to login or register
def index(request):
	all_users = User.objects.all()
	context = {
		"all_users": all_users
	}
	return render(request, 'index.html', context)

#creating User
def register(request):
	if request.method == 'GET':		
		return redirect('/')
	errors = User.objects.basic_validation(request.POST)
	#checking the user entering all info 
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	password = request.POST['password']
	pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
	print(pw_hash)
	newuser = User.objects.create (
		first_name=request.POST['first_name'],
		last_name=request.POST['last_name'],
		email=request.POST['email'],
		address=request.POST['address'],
		zipcode=request.POST['zipcode'],
		state=request.POST['state'],
		password= pw_hash,
	)
	request.session['user_id'] = newuser.id
	#will render new page if successful and will also store user info so they can stay logged in
	return redirect('/success')

#success and checking if a valid user is signed in (user.id)
def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'success.html', context)

#login for exsiting user
def login(request):
	user = User.objects.filter(email=request.POST['email'])
	if user:
		logged_user = user[0]
		if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
			request.session['user_id'] = logged_user.id
			return redirect ('/usershome')
		messages.error(request, 'Invaild Credentials')
		return redirect('/')
	messages.error(request, 'Email or password does not match our records')
	return redirect('/')

# logout for user and returing to sign in page
def logout(request):
	request.session.flush()
	return redirect('/')

# users home page
def usershome(request):
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['user_id'])
	context = {
		'user': user
	}
	return render(request, 'usershome.html', context)

#new order and review page
def neworder(request):
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['user_id'])
	review = Review.objects.all()
	item = Item.objects.all()
	context = {
		'user': user,
		'review': review,
		'item': item,
	}
	return render(request, 'neworder.html', context)

#for people to actual leave a review
def review(request):
	reviewtext = request.POST['review']
	errors = Review.objects.reviewvalidate(reviewtext)
	if len(errors) > 0:
		for key, val in errors.items():
			messages.error(request, val)
	user = User.objects.get(id=request.session['user_id'])
	Review.objects.create(review = reviewtext, user = user)
	return redirect('/neworder')

#comment under reviews
def comment(request):
	comment = request.POST['comment']
	review_id = request.POST['review_id']
	user = User.objects.get(id=request.session['user_id'])
	review = Review.objects.get(id=review_id)
	Comment.objects.create(comment = comment, user = user, review = review)
	return redirect('/neworder')

# Like button, many-to-many
def likes(request, id):
	liked_post = Review.objects.get(id=id)
	likes = User.objects.get(id=request.session['user_id'])
	liked_post.likes.add(likes)
	return redirect('/neworder')

# Webpage to update users own info
def edituser(request):
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['user_id'])
	context = {
		'user': user
	}
	return render(request, 'edituser.html', context)

#to save edits made by user
def editprofile(request, id):
	edit_user = User.objects.get(id = id)
	edit_user.first_name = request.POST['first_name']
	edit_user.last_name = request.POST['last_name']
	edit_user.email=request.POST['email']
	edit_user.address=request.POST['address']
	edit_user.zipcode=request.POST['zipcode']
	edit_user.state=request.POST['state']
	edit_user.save()
	return redirect('/edituser')

# User can delete profile 
def deleteuser(request):
	user = User.objects.get(id=request.session['user_id'])
	user.delete()
	return redirect('/')

#rendering page to add item.
def item(request):
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['user_id'])
	item = Item.objects.all()
	context = {
		'user': user,
		'item': item,
	}
	return render(request, 'item.html', context)	

#adding item function
def additem(request):
	errors = Item.objects.itemvalidate(request.POST)
	if len(errors) > 0:
		for key, val in errors.items():
			messages.error(request, val)
		return redirect('/item')
	Item.objects.create(
		itemname = request.POST['itemname'],
		description = request.POST['description'],
		price = request.POST['price'],
	)
	return redirect('/neworder')

#completed order/cart page render and api call
def complete(request):
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['user_id'])
	last = Order.objects.last()
	price = last.totalprice
	fullorder = Order.objects.aggregate(Sum('orders'))['orders__sum']
	fullprice = Order.objects.aggregate(Sum('totalprice'))['totalprice__sum']
	#api call for project will delete once I get google maps to work 
	r = requests.get(poke_api)
	r = r.json()
	results = r['results']
	# google maps api call not working says json decoding error had <iframe> on html before deleting to make poke_api work
	# looked at python documentation and it said to use w.json.loads(w) but it gives me an error saying response doesn't have load function even if I import json like documentation said.
	# w = requests.get(google_maps_api)
	# w = w.json()
	# res = r['res']
	context = {
		#'maps': res,
		'pokemon': results,
		'user': user,
		'order': fullorder,
		'total': fullprice,
	}
	return render(request, 'complete.html', context)

#pick item to purchase
def pickitem(request):
	if request.method == 'POST':
		#ITEM TO BE PURCHASED = ITP
		itp = Item.objects.filter(id=request.POST['id'])
		if not itp:
			return redirect('/neworder')
		else:
			user = User.objects.get(id=request.session['user_id'])
			quantity = int(request.POST['quantity'])
			total = quantity * (float(itp[0].price))
			Order.objects.create( orders=quantity, totalprice=total, user=user)
			return redirect('/complete')
	else:
		return redirect('/neworder')





