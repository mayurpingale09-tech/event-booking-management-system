from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("update-booking/<int:booking_id>/", views.update_booking, name="update_booking"),
    path('', views.home, name='home'),
    path('events/', views.events_list, name='events'),
    path('services/', views.services_list, name='services'),
    path('bookings/', views.bookings_list, name='bookings'),

    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('contact/', views.contact, name='contact'),

    path('events/<int:event_id>/book/', views.book_event, name='book_event'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('events/<int:event_id>/book/', views.book_event, name='book_event'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),

    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('create/', views.add_event, name='create_event'),
    path('events/<int:event_id>/update/', views.update_event, name='update_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),

    path('add-concert/', views.add_concert, name='add_concert'),
    path('c_list/', views.concert_list, name='concert_list'),
    path('concert/<int:concert_id>/', views.concert_detail, name='concert_detail'),
    path('concert/<int:concert_id>/book/', views.book_ticket, name='book_ticket'),
    path('manage-concerts/', views.manage_concerts, name='manage_concerts'),
    path('verify-payment/<int:booking_id>/', views.verify_payment, name='verify_payment'),
    path('concert/edit/<int:concert_id>/', views.edit_concert, name='edit_concert'),
    path('concert/delete/<int:concert_id>/', views.delete_concert, name='delete_concert'),
    path('update-c-booking/<int:booking_id>/', views.update_c_booking, name='update_c_booking'),
]



# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)