from django.urls import path
from .views import CareerListView, CareerDetailView

urlpatterns = [
    path('', CareerListView.as_view(), name='career-list'),
    path('<slug:slug>/', CareerDetailView.as_view(), name='career-detail'),
]
