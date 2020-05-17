from django.urls import path

import dashboard
from dashboard.views import home, RequestCreateView, RequestDetailView, RequestUpdateView, RequestDeleteView

urlpatterns = [
    path('',home, name='home'),
    path('request/new/',RequestCreateView.as_view,name='request_create'),
    path('request/<int:pk>/', RequestDetailView.as_view, name='request_create'),
    path('request/edit/<int:pk>/', RequestUpdateView.as_view, name='request_create'),
    path('request/delete/<int:pk>/', RequestDeleteView.as_view, name='request_create'),

]