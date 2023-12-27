"""
URL configuration for Ask_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:question_id>', views.question, name='question'),
    path('hot/', views.hot, name='hot'),
    path('tag/<tag_name>', views.tag, name='tag'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('profile/edit/', views.settings, name='settings'),
    path('admin/', admin.site.urls),
    # path('like', views.like, name='like'),
    # path('correctanswer', views.correct_answer, name='correct_answer')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


