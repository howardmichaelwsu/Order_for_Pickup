from django.shortcuts import render, redirect

# home page render
def index(request):
	return render(request, "index.html")
# Create your views here.
