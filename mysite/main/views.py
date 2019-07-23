from django.shortcuts import render, redirect
from .models import Essay, EssaySeries, EssayCategory
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User		# for community tab purpose
from django.contrib.sessions.models import Session
from django.utils import timezone
from .forms import Write_content, ContactForm


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
		# return HttpResponse('<script>history.back();</script>')
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
				return HttpResponse('<script>javascript:history.go(-2);</script>')
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
	if request.user.is_authenticated:
		active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
		user_id_list = []
		for session in active_sessions:
			data = session.get_decoded()
			user_id_list.append(data.get('_auth_user_id', None))
		# Query all logged in users based on id list
		users =  User.objects.filter(id__in=user_id_list)
		return render(request=request, 
					template_name="main/community.html",
					context={"users": users},
					)
	else:
		messages.warning(request, f"For Community Login first!")
		return redirect("main:login")
				 
				 
def account(request):
	if request.user.is_authenticated:
		return render(request=request, 
				  template_name="main/account.html",
				 )
	else:
		return redirect("main:login")

# this is used for testing for new features
def experiment(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = ContactForm()
    return render(request, 'main/experiment.html', {'form': form})


def write_request(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			form = Write_content(request.POST, request.FILES)
			if form.is_valid():
				obj = form.save(commit=False)
				# Generating single slug
				try:
					series = "".join(filter(str.isalpha, map(lambda x: x[0], str(form.cleaned_data.get('series_title')).split(" ")))).upper()
					title = form.cleaned_data.get('essay_title')
					obj.essay_slug = series + "-" + "-".join(title.split(" ")[:4]).lower()
					obj.save()
					form.save(commit=True)
					# current_series = EssaySeries.objects.get(series_title=obj.series_title)
					messages.success(request, f"Content Written Successfully!")
					# messages.error(request, f"{obj.essay_slug}")
					return redirect("/"+obj.essay_slug)
				except Exception as ex:
					messages.error(request, f"Please feedback error{ex}")
					return redirect("main:write_content")
			else:
				messages.error(request, f"Please Write Content!")

				return render(request=request,
								template_name="main/user_write.html",
								context={"form": form})
		form = Write_content
		return render(request=request, 
					template_name="main/user_write.html",
					context={"form":form}
					)
	else:
		messages.warning(request, f"For Community Login first!")
		return redirect("main:login")