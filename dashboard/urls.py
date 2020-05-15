from django.urls import path

import dashboard
from dashboard.views import home

urlpatterns = [
    path('',home, name='home'),
]