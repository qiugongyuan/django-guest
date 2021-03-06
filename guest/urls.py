"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from sign import views #导入sign应用views文件
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),#添加index/路径配置
    path('login_action/',views.login_action),
    path('event_manage/',views.event_manage),
    path('accounts/login/',views.index),
    path('search_name/',views.search_name),
    path('guest_manage/',views.guest_manage),
    path('search_phone/',views.search_phone),
    #path('logout/',views.logout),
    url (r'^logout/$', views.logout),
    url(r'^sign_index/(?P<event_id>[0-9]+)/$', views.sign_index),
    url(r'^sign_index_action/(?P<event_id>[0-9]+)/$', views.sign_index_action),
    url(r'^api/',include(('sign.urls','sign'),namespace="sign")),


]
