from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path('', views.homepage, name="homepage"),
	path('logout', views.logout_request, name="logout"),
	path('login', views.login_request, name="login"),
	path('register', views.register, name="register"),
	path('about', views.about, name="about"),
	path('community', views.community, name="community"),
	path('account', views.account, name="account"),
	path('experiment', views.experiment, name="experiment"),
	path('<single_slug>', views.single_slug, name="single_slug"),
]
