from django.urls import path

import dashboard
from dashboard.views import home, RequestCreateView, RequestDetailView, RequestUpdateView, RequestDeleteView, \
    RequestListView, RequestDeanView, RequestDeleteDView, RequestUpdateDView

urlpatterns = [
    path('',home, name='home'),
    path('requests/',RequestListView.as_view(),name='request_list'),
    path('requests_change/',RequestDeanView.as_view(),name='requests_change'),
    path('request/new/',RequestCreateView.as_view(),name='request_create'),
    path('request/<int:pk>/', RequestDetailView.as_view(), name='request_detail'),
    path('request/edit/<int:pk>/', RequestUpdateView.as_view(), name='request_update'),
    path('request/delete/<int:pk>/', RequestDeleteView.as_view(), name='request_delete'),
    path('request/dean_delete/<int:pk>/',RequestDeleteDView.as_view(),name='dean_delete'),  #URL must be unique!
    path('request/dean_edit/<int:pk>/', RequestUpdateDView.as_view(), name='dean_update'),

]