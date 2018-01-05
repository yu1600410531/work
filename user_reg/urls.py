"""user_reg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from home import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^reg/$',views.register,name='reg'),
    url(r'^login/$',views.log_in,name='login'),
    url(r'^address/$',views.address,name='address'),


    url(r'^payment/$',views.get_payment,name='payment'),

    url(r'^order/(?P<id>\d+)',views.order,name='order'),
    url(r'^alluser/$',views.all_user,name='alluser'),
    url(r'^queren/(?P<id>\d+)',views.Queren,name='queren'),
    url(r'^hetong/(?P<id>\d+)',views.Hetong,name='hetong'),

    url(r'userlogin',views.userlogin,name='userlogin'),
    url(r'userlogout',views.userlogout,name='userlogout')


]
