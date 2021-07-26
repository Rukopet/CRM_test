from django.urls import path

from .views import documentation, Clients, Bids

urlpatterns = [
    path('documentation/', documentation, name="documentation_url"),
    path('clients/<int:client_id>/change/<str:field>=<str:value>/', Clients.change_client),
    path('clients/<int:client_id>/delete/', Clients.remove_client),
    path('clients/<int:client_id>/', Clients.show_one),
    path('clients/create/<str:name>&<str:telegram>/', Clients.create_client),
    path('clients/create/', Clients.as_view()),
    path('clients/', Clients.show_all),


    path('bids/', Bids.show_all),
    path('bids/create/', Bids.as_view()),
    path('bids/create/<int:type_bid>&<int:client_id>&<str:body>&<slug:title_bid>&<int:notifications>/', Bids.create_bid),
    path('bids/<int:bid>/', Bids.show_one),
    path('bids/<str:category>/', Bids.show_category)
]