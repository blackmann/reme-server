from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^popular/', views.popular),
    url(r'^recent/', views.recent),
    url(r'^similar/(?P<reme_id>\d+)/', views.similar),
    url(r'^download/(?P<reme_id>\d+)/', views.download),
    url(r'^upload/', views.upload),
    url(r'^search/', views.search)
]