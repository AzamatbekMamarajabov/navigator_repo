"""This file is for urls used in app """
from django.urls import path
from .views import HomeSearchView, csv_download_view
urlpatterns = [
    path('', HomeSearchView.as_view(), name='home'),
    path('download/', csv_download_view, name='download')
]
