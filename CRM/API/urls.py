from django.urls import path

from .views import documentation
from ..API.views import bids_list

urlpatterns = [
    path('documentation/', documentation, name="documentation_url"),
    path('', bids_list, name='CRM_url')
]