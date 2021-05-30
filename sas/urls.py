from django.contrib import admin
from django.urls import path
from .views import DetailDecisionsView, CheckRulesSetView, CheckLookups, DecisionsView, GetRTDMData


urlpatterns = [
    path('myvmeste_admin/', admin.site.urls),
    path('', GetRTDMData.as_view(), name='get_rtdm'),
    path('get_decisions', DecisionsView.as_view(), name='get_decisions'),
    path('get_detail_decisions', DetailDecisionsView.as_view(), name='get_detail_decisions'),
    path('check_rules_sets', CheckRulesSetView.as_view(), name='check_rules_sets'),
    path('check_lookups', CheckLookups.as_view(), name='check_lookups'),
]
