from django.shortcuts import render, redirect
from .models import Essay, EssaySeries
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def single_slug(request, single_slug):
	series = [s.series_slug for s in EssaySeries.objects.all()]
	if single_slug in series:
		matching_essay = Essay.objects.filter(series_title__series_slug=single_slug)
		essay_urls = {}
		for m in matching_essay.all():
			essay_urls[m] = m.essay_slug
		return render(request=request,
					  template_name='main/home.html',
					  context={"essays": matching_essay, "part_one": essay_urls}
					  )
	return render(request=request,
				  template_name='main/under_construction.html',
				  context={"pagename":single_slug}
				 )
	

def experiment(request):
	if request.user.is_authenticated:
		return render(request=request,
				  template_name='main/experiment.html',
				 )
	else:
		return redirect("main:about")


# Create your views here.
def homepage(request):
	return render(request=request, 
				  template_name="main/series.html",
				  context={"series":EssaySeries.objects.all}
				 )
				 
				
def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("main:homepage")
	
	
def login_request(request):
	if request.user.is_authenticated:
		return redirect("main:account")
	if request.method == "POST":
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}")
				return redirect("/")
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, 
				  template_name="main/login.html",
				  context={"form":form}
				 )
				 
				 
def register(request):
	if request.user.is_authenticated:
		return redirect("main:account")
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"New account created: {username}")
			login(request, user)
			return redirect("/")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages[msg]}")

				return render(request=request,
								template_name="main/register.html",
								context={"form": form})
	form = UserCreationForm
	return render(request=request, 
				  template_name="main/register.html",
				  context={"form":form}
				 )
				 
def about(request):
	return render(request=request, 
				  template_name="main/about.html",
				 )
				 
				 
def community(request):
	return render(request=request, 
				  template_name="main/community.html",
				 )
				 
				 
def account(request):
	return render(request=request, 
				  template_name="main/account.html",
				 )