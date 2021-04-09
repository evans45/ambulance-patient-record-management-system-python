from django.urls import path
from . import views



urlpatterns = [
    path('paramedichome',views.parahom, name = 'paramedichome'),
    path('adminlogin',views.adminlogin, name = 'adminlogin'),
    path('hospitalhome',views.hoshome, name = 'hospitalhome'),
    path('patientreport',views.patrepo, name = 'patientreport'),
    path('patientdetails',views.patdetails, name = 'patientdetails'),
    path('analysis',views.analysis, name = 'analysis'),    
    path('chat',views.chat, name = 'chat'),
    path('pdf',views.topdf, name = 'pdf'),
    path('addhos',views.addhos, name = 'addhos'),
    path('',views.home, name = 'home'),
    path('login',views.login, name = 'login'),
    path('hosanapage',views.hosanapage, name = 'hosanapage'),
    path('changepassword',views.passchange, name = 'changepassword'),
    path('change',views.changepass, name = 'change'),
    path('cause',views.getcause, name = 'cause'),
    path('hosanalytics',views.hosanalytics, name = 'hosanalytics'),
    path('head',views.head, name = 'head'),
    path('logoutr',views.logoutr, name = 'logoutr'),
    path('search',views.search, name = 'search'),
    path('delete',views.delete, name = 'delete'),
    path('update',views.update, name = 'update')
]