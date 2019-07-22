from django.shortcuts import render, redirect
from .models import Essay, EssaySeries, EssayCategory
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def single_slug(request, single_slug):
	# First we search any url in category and then series after that main content
	categories = [c.category_slug for c in EssayCategory.objects.all()]
	if single_slug in categories:
		matching_series = EssaySeries.objects.filter(category_title__category_slug=single_slug)	
		this_category = EssayCategory.objects.get(category_slug=single_slug)
		return render(request=request,
						template_name="main/series.html",
						context={"series":matching_series.all(), "category": this_category}
						)
	# now searching url in series
	series = [s.series_slug for s in EssaySeries.objects.all()]
	if single_slug in series:
		matching_essay = Essay.objects.filter(series_title__series_slug=single_slug)
		# for navbar
		this_series = EssaySeries.objects.get(series_slug=single_slug)
		return render(request=request,
					  template_name='main/essays.html',
					  context={"essays": matching_essay.all(), "series": this_series}
					  )

	# Now we are going to main content
	essays = [e.essay_slug for e in Essay.objects.all()]
	if single_slug in essays:
		this_essay = Essay.objects.get(essay_slug=single_slug)
		this_series = EssaySeries.objects.get(series_title=this_essay.series_title)
		this_category = EssayCategory.objects.get(category_title=this_series.category_title)

		essay_from_series = Essay.objects.filter(series_title__series_title=this_essay.series_title).order_by('essay_published')
		this_essay_idx = list(essay_from_series).index(this_essay)


		return render(request = request,
						template_name='main/essay.html',
						context = {"essay":this_essay, "category": this_category.category_title,
								   "sidebar": essay_from_series,
                               	   "this_essay_idx": this_essay_idx,
								   })

	# If slug doesn't exist anywhere then
	messages.warning(request, "Kaha Chal Diye Guru!!????")
	return render(request=request,
				template_name='main/under_construction.html',
				context={"pagename":single_slug}
				)
		# For testing Purpose
		# matching_essay = list(map(lambda x: x.essay_title, matching_essay))  
		# for i in EssaySeries.objects.all():
		# 	if i.series_slug == single_slug:
		# 		matching_series = i.series_title
		# 		break
		# matching_essays_slug = []
		# for e in Essay.objects.all():
		# 	if e.series_title.series_title == matching_series:
		# 		matching_essays_slug.append(e.essay_slug)
		# return HttpResponse("Series Hai: " + str(matching_essay) + str(essay_urls))
	

def homepage(request):
	return render(request=request, 
				  template_name="main/home.html",
				  context={"category":EssayCategory.objects.all}
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
	if request.user.is_authenticated:
		return render(request=request, 
				  template_name="main/account.html",
				 )
	else:
		return redirect("main:login")

# this is used for testing for new features
def experiment(request):
	if request.user.is_authenticated:
		return render(request=request,
				  template_name='main/experiment.html',
				 )
	else:
		return redirect("main:about")