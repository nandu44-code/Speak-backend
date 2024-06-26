from django.urls import path,include
from .views import (
                    SlotListCreateView,
                    SlotFilterView,
                    SlotDetailView,
                    BookingView,
                    GetBookingsStudent,
                    BookingDeleteView,
                    get_all_bookings,
                    SlotsBookingViewSet,
                    BookingCancelView,
                    BookingCreateView,
                    get_all_bookings_count,
                    get_all_slots_count
                    )
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'booking-view', BookingView)
router.register(r'bookings-listing', SlotsBookingViewSet, basename='bookings')


urlpatterns = [
    path('', include(router.urls)),
    path('slots/',SlotListCreateView.as_view(), name='slot-list-create'),
    path('slots/<int:pk>/', SlotDetailView.as_view(), name='slot-detail'),
    path('slots/filter/', SlotFilterView.as_view(), name='slot-filter'),
    # path('bookings/filter/<int:tutor>/<str:status>', GetBookings),
    path('student/bookings/filter/<int:user>/<str:status>', GetBookingsStudent),
    path('booking/<int:slot>/delete/', BookingDeleteView.as_view(), name='booking-delete'),
    path('booking/<int:slot>/cancel/', BookingCancelView.as_view(), name='booking-delete'),
    path('bookings-all/', get_all_bookings, name='get_all_bookings'),
    path('bookings/create/', BookingCreateView.as_view(), name='create-booking'),
    path('bookings-count/', get_all_bookings_count, name="booking-count"),
    path('slots-count/<int:tutor>/', get_all_slots_count, name='slots-count')

]


