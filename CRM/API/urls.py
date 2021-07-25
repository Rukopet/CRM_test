from django.urls import path

from .views import documentation, clients_show_all, clients_show_one

urlpatterns = [
    path('documentation/', documentation, name="documentation_url"),
    path('clients/<str:client_id>/', clients_show_one),
    path('clients/<str:client_id>/delete/', client_delete)
    path('clients/', clients_show_all)
]
