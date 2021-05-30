from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

#home page to login or registe
def index(request):
	all_users = User.objects.all()
	context = {
		"all_users": all_users
	}
	return render(request, 'index.html', context)

#creating User
def register(request):
	if request.method == 'POST':		
		errors = User.objects.basic_validation(request.POST)
	#checking the user entering all info
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value)
			return redirect('/')
		
		first_name=request.POST['first_name']
		last_name=request.POST['last_name']
		email=request.POST['email']
		address=request.POST['address']
		zipcode=request.POST['zipcode']
		state=request.POST['state'] 
		password=request.POST['password']
		hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
		User.objects.create(first_name=first_name, last_name=last_name, email=email, address=address, zipcode=zipcode,state=state, password=hash_pw)
	#will render new page if successful and will also store user info so they can stay logged in
		return redirect('/success')

#success and checking if a user.id is in session
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
    user = User.objects.filter(email = request.POST['email'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['user_id'] = userLogin.id
            return redirect('/success/')
        messages.error(request, 'Invalid Credentials')
        return redirect('/')
    messages.error(request, 'That Username is not in our system, please register for an account')
    return redirect('/')

# logout for user and returing home
def logout(request):
	request.session.flush()
	return redirect('/')
