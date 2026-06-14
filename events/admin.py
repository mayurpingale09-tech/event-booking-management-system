from django.contrib import admin
from .models import Event, Service, Booking, Review,Concert,C_Booking,Payment,ContactMessage

admin.site.register(Event)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Concert)
admin.site.register(C_Booking)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(ContactMessage)


