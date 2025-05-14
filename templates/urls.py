"""
URL configuration for CORE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from uap.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('home/', home, name='home'),
    path("post/", post_complaint, name="post_complaint"),
    path("my-responses/", complaint_responses_and_feedback, name="complaint_responses"),
    path("faq/", university_faq, name="university_faq"),

    path("authority/login/", authority_login, name="authority_login"),
    path("authority/logout/", authority_logout, name="authority_logout"),
    path("authority/dashboard/", authority_dashboard, name="authority_dashboard"),
    path("authority/complaint/<int:complaint_id>/respond/", respond_to_complaint, name="respond_complaint"),
    path("authority/complaint/<int:complaint_id>/feedback/", view_feedback, name="view_feedback"),

    
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
