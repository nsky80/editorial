from django.urls import path
from . import views
from django.conf import settings # for images handling
from django.conf.urls.static import static 

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
	path('write_content', views.write_request, name="write_content"),
	path('<single_slug>', views.single_slug, name="single_slug"),
]

# if settings.DEBUG:
#         urlpatterns += static(settings.MEDIA_URL,
#                               document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
