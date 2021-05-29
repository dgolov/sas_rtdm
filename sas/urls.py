from django.urls import path
from .views import DetailDecisionsView


urlpatterns = [
    path('get_detail_decisions', DetailDecisionsView.as_view(), name='get_detail_decisions'),
]