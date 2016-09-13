from django.conf.urls import url
from cnoapp import views

urlpatterns = [
    url(r'^add_user/$', views.add_user),
    url(r'^add_master/$', views.add_master),
    url(r'^get_menu/$', views.menu_list),
    url(r'^get_user/(?P<fbid>[0-9]+)/$', views.get_user),
    url(r'^place_order/$', views.place_order),    
    url(r'^confirm_order/$', views.accept_order),
    url(r'^update_gcm/$', views.update_gcm),
]