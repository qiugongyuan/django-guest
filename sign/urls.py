from django.conf.urls import url
from sign import views_if
from sign import views_if_sec

urlpatterns={
    #sign system interface:
    #ex: /api/add_event/
    url(r'^add_event/',views_if.add_event,name='add_event'),
    #
    # ex:/api/add_guest/
    url(r'^add_guest/', views_if.add_guest, name='add_guest'),
    #
    # ex: / api /get_event_list/
    url(r'^get_event_list/', views_if.get_event_list, name='get_event_list'),
    #
    # ex: /api/get_guest_list/
    url(r'^get_guest_list/', views_if.get_guest_list, name='get_guest_list'),
    #
    # ex:/api/user_sign/
     url(r'^user_sign/', views_if.user_sign, name='user_sign'),
    #ex:/api/sec_get_event_list/
    url(r'^get_sec_event_list/',views_if_sec.get_sec_event_list,name='get_sec_event_list'),

    # ex:/api/add_sec_event/
    url(r'^add_sec_event/', views_if_sec.add_sec_event, name='add_sec_event')

}