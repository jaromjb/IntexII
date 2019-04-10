from django.urls import path
from .views import create_prescriber, update_prescriber, delete_prescriber

urlpatterns = [
    path('new', create_prescriber, name='create_prescriber'),
    path('update/<int:id>/', update_prescriber, name='update_prescriber'),
    pathe('delete/<ind:id>/', delete_prescriber, name='delete_prescriber'),
]