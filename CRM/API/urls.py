from datetime import datetime
from django.urls import path, register_converter

from .views import documentation, Clients, Bids, Staff


class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value


# class ApiKeyConverter:
#     pass


register_converter(DateConverter, 'yyyy')

urlpatterns = [

    path('documentation/', documentation, name="documentation_url"),
    path('clients/<int:client_id>/change/<str:field>=<str:value>/', Clients.change_client),
    path('clients/<int:client_id>/delete/', Clients.remove_client),
    path('clients/<int:client_id>/', Clients.show_one),
    path('clients/create/<slug:name>&<slug:telegram>/', Clients.create_client),
    path('clients/create/', Clients.as_view()),
    path('clients/', Clients.show_all),

    path('bids/', Bids.show_all),
    path('bids/create/', Bids.as_view()),
    path('bids/create/<int:type_bid>&<int:client_id>&<str:body>&<slug:title_bid>&<int:notifications>/',
         Bids.create_bid),
    path('bids/<int:bid>/change/<str:field>=<str:value>/', Bids.change_one),
    path('bids/<int:bid>/', Bids.show_one),
    path('bids/<str:category>/', Bids.show_category),
    path('bids/dates/<yyyy:date>/', Bids.show_date),
    path('bids/dates/<yyyy:date>/<yyyy:up_date>/', Bids.show_dates),

    path('staff/', Staff.show_all),
    path('staff/<int:staff_id>/', Staff.show_one),
    path('staff/create/<str:slug>/', Staff.create_one),
    path('staff/create/', Staff.as_view()),
    path('staff/<int:staff_id>/delete/', Staff.delete_one),
    path('staff/<int:staff_id>/change/<str:field>=<str:value>/', Staff.change_one),

]
