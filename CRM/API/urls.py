from django.urls import path

from .views import documentation, Clients

urlpatterns = [
    path('documentation/', documentation, name="documentation_url"),
    path('clients/<int:client_id>/change/<str:field>=<str:value>/', Clients.change_client),
    path('clients/<int:client_id>/delete/', Clients.remove_client),
    path('clients/<int:client_id>/', Clients.show_one),
    path('clients/create/<str:name>&<str:telegram>/', Clients.create_client),
    path('clients/create/', Clients.bad_request_check_documents),
    path('clients/', Clients.show_all)
]
