from django.urls import path

from .views import documentation, clients

urlpatterns = [
    path('documentation/', documentation, name="documentation_url"),
    path('clients/<str:client_id>/', clients.show_one),
    path('clients/<str:client_id>/delete/', clients.remove_client),
    path('clients/create/<str:name>&<str:telegram>/', clients.create_client),
    path('clients/create/', clients.create_client),
    path('clients/', clients.show_all)
]
