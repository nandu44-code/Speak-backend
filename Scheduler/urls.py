from django.urls import path
from .views import SlotListCreateView,SlotFilterView,SlotDetailView

urlpatterns = [
    path('slots/',SlotListCreateView.as_view(), name='slot-list-create'),
    path('slots/<int:pk>/', SlotDetailView.as_view(), name='slot-detail'),
    path('slots/filter/', SlotFilterView.as_view(), name='slot-filter'),
]
