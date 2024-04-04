from django.urls import path
from .views import SlotListCreateView,SlotFilterView,SlotDetailView,BookingView,GetBookings,GetBookingsStudent,BookingDeleteView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'bookings', BookingView)

urlpatterns = [
    path('slots/',SlotListCreateView.as_view(), name='slot-list-create'),
    path('slots/<int:pk>/', SlotDetailView.as_view(), name='slot-detail'),
    path('slots/filter/', SlotFilterView.as_view(), name='slot-filter'),
    path('bookings/filter/<int:tutor>/<str:status>', GetBookings),
    path('student/bookings/filter/<int:user>/<str:status>', GetBookingsStudent),
    path('booking/<int:slot>/delete/', BookingDeleteView.as_view(), name='booking-delete')
]


