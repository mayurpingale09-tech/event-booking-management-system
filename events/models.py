from django.db import models
from django.contrib.auth.models import User

# Event Categories
EVENT_CATEGORIES = [
    ('CULTURAL', 'Cultural'),
    ('CORPORATE', 'Corporate/Business'),
    ('SPORTS', 'Sports'),
    ('SOCIAL', 'Social'),
    ('EDUCATIONAL', 'Educational'),
    ('CHARITY', 'Charity/Fundraising'),
]

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EVENT_CATEGORIES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return self.title


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateField()
    event_time = models.TimeField()  # Time for the event, like 18:30
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    guest_count = models.PositiveIntegerField(default=20)
    additional_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default="Pending", choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Cancelled", "Cancelled")])
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number field
    email = models.EmailField(blank=True, null=True)  # Optional email field

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    feedback = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} on {self.event.title}"

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to User
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


from django.db import models
from django.contrib.auth.models import User

class Concert(models.Model):
    name = models.CharField(max_length=255)  # Concert name
    description = models.TextField()  # Concert details
    date = models.DateTimeField()  # Date and time of the concert
    venue = models.CharField(max_length=255)  # Venue name
    address = models.TextField()  # Full address
    city = models.CharField(max_length=100)  # City
    state = models.CharField(max_length=100, blank=True, null=True)  # State (optional)
    country = models.CharField(max_length=100)  # Country
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)  # Ticket price
    total_tickets = models.PositiveIntegerField()  # Total tickets available
    available_tickets = models.PositiveIntegerField()  # Remaining tickets
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)  # Google Pay QR code uploaded by admin
    image = models.ImageField(upload_to='concert_images/', blank=True, null=True)  # Concert banner
    created_at = models.DateTimeField(auto_now_add=True)  # Created timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Updated timestamp

    def __str__(self):
        return f"{self.name} - {self.date.strftime('%Y-%m-%d')}"

    def book_tickets(self, quantity):
        """ Reduce available tickets when a booking is made. """
        if quantity > self.available_tickets:
            raise ValueError("Not enough tickets available")
        self.available_tickets -= quantity
        self.save()

class C_Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who booked the ticket
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)  # Concert being booked
    quantity = models.PositiveIntegerField()  # Number of tickets booked
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price paid
    transaction_id = models.CharField(max_length=50, blank=True, null=True)  
    booking_date = models.DateTimeField(auto_now_add=True)  # Booking timestamp
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending Payment'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
        default='pending'
    )  # Status of booking

    def __str__(self):
        return f"{self.user.username} - {self.concert.name} ({self.quantity} tickets)"

    def save(self, *args, **kwargs):
        """ Automatically update concert ticket availability on booking. """
        if self.pk is None:  # Only reduce tickets on new booking
            self.concert.book_tickets(self.quantity)
        super().save(*args, **kwargs)

class Payment(models.Model):
    booking = models.OneToOneField(C_Booking, on_delete=models.CASCADE)  # Link payment to booking
    transaction_id = models.CharField(max_length=100, unique=True)  # Transaction ID entered by user
    payment_date = models.DateTimeField(auto_now_add=True)  # Payment timestamp
    verified = models.BooleanField(default=False)  # Admin verifies transaction

    def __str__(self):
        return f"Payment for {self.booking.concert.name} - {self.transaction_id}"

    def mark_as_verified(self):
        """ Mark payment as verified and confirm booking. """
        self.verified = True
        self.booking.status = 'confirmed'
        self.booking.save()
        self.save()

from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
