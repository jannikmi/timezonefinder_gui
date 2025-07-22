"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
# from django.http import HttpResponseRedirect
# from django.contrib import admin
from API.views import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^api/(?P<mode>\d)_(?P<lng>[-]?\d+(\.\d*)?)_(?P<lat>[-]?\d+(\.\d*)?)$', api_request),
    url(r'^api/.*$', api_bad_request),
    url(r'^gui$', main_gui_view_fresh),
    url(r'^gui/getInfo/(?P<tz_name>.+)$', gui_get_info),
    url(r'^gui/getGeometry/(?P<tz_name>.+)$', gui_get_geometry),
    # url(r'^gui/getGeometry/(.+)/?(.+)?/?(.+)?$', gui_get_geometry),
    # url(r'^gui/getGeometry/(?P<tz_name>(\w+[_/]?)+)$', gui_get_geometry),
    url(r'^gui/(?P<mode>\d)_(?P<lng>[-]?\d+(\.\d*)?)_(?P<lat>[-]?\d+(\.\d*)?)$', main_gui_view),
    url(r'^statistic$', statistic_view),
    url(r'^api_guide$', static_api_guide_view),
    # everything else is redirected to a fresh main gui view
    url(r'^.*$', redirect2fresh_gui),
]
