from django.conf.urls import url

from . import views

app_name = 'anagrafica'
urlpatterns = [
    url(r'^$', views.anagrafica),
]
