
text/x-generic urls.py ( Python script, ASCII text executable, with CRLF line terminators )
"""sendsms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from message.admin import CustomAdminSite
from django.urls import path,include
from message.views import chart_view
admin.site.__class__ = CustomAdminSite
from django.contrib.admin.views.decorators import staff_member_required

from django.urls import path
from message import views
from message.views import logins
admin.site.login = logins


    




urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin/',admin.CustomAdminSite.urls),
    path('admin/chart/', staff_member_required(views.chart_view), name='admin_chart'),
    # path('admin/chart/',chart_view,name='chart'),
    # path('admin/chart', admin.site.admin_view(chart_view), name='message_chart'),
    path('',include('message.urls')),
    path('', include('django.contrib.auth.urls')),
    
]





