"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from accounts.views import main_view
from quiz.views import quiz_detail, quiz, search_quizzes, edit, delete_quiz
from django.conf.urls.static import static
from accounts.views import logout_view, login_view, register_view, create


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='main_page'),
    path("quizzes", search_quizzes, name="quizzes"),
    path("<int:pk>/quiz", quiz, name="quiz"),
    path('create/', create, name='create'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('quizzes/<int:pk>/edit/', edit, name='edit'),
    path("quizzes/<int:pk>/delete/", delete_quiz, name="delete_quiz"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)