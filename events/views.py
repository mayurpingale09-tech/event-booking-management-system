from django.shortcuts import render
from .models import Event, Service, Booking
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event,ContactMessage

# View all events
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

# View event details
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

# Create an event (Admin only)
@login_required
def create_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        category = request.POST['category']
        price = request.POST['price']
        image = request.FILES.get('image')

        Event.objects.create(
            title=title,
            description=description,
            category=category,
            price=price,
            image=image
        )

        messages.success(request, "Event created successfully!")
        return redirect('event_list')

    return render(request, 'events/create_event.html')

# Update an event (Admin only)
@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event.title = request.POST['title']
        event.description = request.POST['description']
        event.category = request.POST['category']
        event.price = request.POST['price']

        if 'image' in request.FILES:
            event.image = request.FILES['image']

        event.save()
        messages.success(request, "Event updated successfully!")
        return redirect('event_detail', event_id=event.id)

    return render(request, 'events/update_event.html', {'event': event})

# Delete an event (Admin only)
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, "Event deleted successfully!")
    return redirect('event_list')

def home(request):
    return render(request, 'home.html')

def events_list(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def services_list(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

def bookings_list(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)
    else:
        bookings = []
    return render(request, 'bookings.html', {'bookings': bookings})


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Signup View
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST['phone']
        address = request.POST['address']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already in use!")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.userprofile.phone = phone
                user.userprofile.address = address
                user.userprofile.save()

                login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Passwords do not match!")
    
    return render(request, 'signup.html')


# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Booking
from django.contrib import messages

# # Event List View
# def events_list(request):
#     events = Event.objects.all()
#     return render(request, 'events_list.html', {'events': events})

from django.shortcuts import render
from .models import Event, EVENT_CATEGORIES

def events_list(request):
    events_by_category = {}

    for category, category_display in EVENT_CATEGORIES:
        events = Event.objects.filter(category=category)
        if events.exists():
            events_by_category[events] = category_display

    return render(request, "events_list.html", {"events_by_category": events_by_category})


# Event Detail & Booking View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, Booking
from datetime import datetime

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event_date = request.POST['event_date']
        event_time = request.POST['event_time']
        guest_count = request.POST.get('guest_count', 1)
        additional_requests = request.POST.get('additional_requests', '')
        location = request.POST['location']
        phone_number = request.POST.get('phone_number', '')
        email = request.POST.get('email', '')

        # Calculate total price (Assuming price per guest)
        total_price = event.price * int(guest_count)

        # Create Booking
        Booking.objects.create(
            user=request.user,
            event=event,
            event_date=event_date,
            event_time=event_time,
            guest_count=guest_count,
            additional_requests=additional_requests,
            total_price=total_price,
            location=location,
            phone_number=phone_number,
            email=email,
        )

        messages.success(request, "Event booked successfully!")
        return redirect('my_bookings')

    return render(request, 'book_event.html', {'event': event})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    c_bookings = C_Booking.objects.filter(user=request.user).order_by('-booking_date')

    return render(request, 'my_bookings.html', {'bookings': bookings,"c_bookings":c_bookings})

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("event_list")

    events = Event.objects.all()
    bookings = Booking.objects.all()
    users = User.objects.all()
    c_bookings=C_Booking.objects.all()
    concerts= Concert.objects.all()
    contact = ContactMessage.objects.all().order_by('-created_at') 

    return render(request, "dashboard.html", {
        "events": events,
        "bookings": bookings,
        "users": users,
        "c_bookings":c_bookings,
        "concerts":concerts,
        "contact":contact

    })


@login_required
def update_booking(request, booking_id):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("admin_dashboard")

    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        booking.status = request.POST["status"]
        booking.save()
        messages.success(request, "Booking status updated successfully!")
        return redirect("admin_dashboard")

    return render(request, "update_booking.html", {"booking": booking})

from .forms import EventForm

@login_required
def add_event(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("home")

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event added successfully!")
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Error adding event. Please try again.")
    else:
        form = EventForm()

    return render(request, "create_event.html", {"form": form})

@login_required
def update_event(request, event_id):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("home")

    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Error updating event. Please try again.")
    else:
        form = EventForm(instance=event)

    return render(request, "update_event.html", {"form": form, "event": event})


@login_required
def delete_event(request, event_id):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("home")

    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect("admin_dashboard")

    return render(request, "delete_event.html", {"event": event})

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Concert
from .forms import ConcertForm  # Import the form for concert creation

  # Restrict access to only staff (admins)
def add_concert(request):
    if request.method == "POST":
        form = ConcertForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Concert added successfully!")
            return redirect('concert_list')  # Redirect to concert list page
    else:
        form = ConcertForm()

    return render(request, 'add_concert.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Concert, C_Booking, Payment
from django.utils.timezone import now

# List all upcoming concerts
def concert_list(request):
    concerts = Concert.objects.filter(date__gte=now()).order_by('date')
    return render(request, 'concert_list.html', {'concerts': concerts})

# View concert details and booking form
def concert_detail(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    return render(request, 'concert_detail.html', {'concert': concert})
import re
from django.core.exceptions import ValidationError
import re
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction  # ✅ Correct import
from .models import Concert, C_Booking

# Define a pattern for the transaction ID (Example: 10 alphanumeric characters)
TRANSACTION_ID_PATTERN = r'^[A-Za-z0-9]{12,14}$'

@login_required
def book_ticket(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)

    if request.method == "POST":
        quantity_str = request.POST.get('quantity')
        transaction_id = request.POST.get('transaction_id')

        # Validate quantity
        if not quantity_str or not quantity_str.isdigit():
            messages.error(request, "Quantity must be a valid number.")
            return redirect('concert_detail', concert_id=concert.id)

        quantity = int(quantity_str)

        if quantity <= 0:
            messages.error(request, "Quantity must be greater than zero.")
            return redirect('concert_detail', concert_id=concert.id)

        # Check if enough tickets are available
        if quantity > concert.available_tickets:
            messages.error(request, "Not enough tickets available.")
            return redirect('concert_detail', concert_id=concert.id)

        # Check if transaction_id is provided
        if not transaction_id:
            messages.error(request, "Transaction ID is required.")
            return redirect('concert_detail', concert_id=concert.id)

        # Validate transaction ID format
        if not re.match(TRANSACTION_ID_PATTERN, transaction_id):
            messages.error(request, "Transaction ID is invalid. It must be 10 alphanumeric characters.")
            return redirect('book_ticket', concert_id=concert.id)

        # Calculate total price
        total_price = quantity * concert.ticket_price

        try:
            with transaction.atomic():
                
                # Create a booking entry with status 'pending'
                C_Booking.objects.create(
                    user=request.user,
                    concert=concert,
                    quantity=quantity,
                    total_price=total_price,
                    transaction_id=transaction_id,  # ✅ Store transaction ID
                    status='pending'  # ✅ Admin will verify later
                )

                # Reduce available tickets count
                concert.available_tickets -= quantity-1
                concert.save()

            messages.success(request, "Booking submitted! Waiting for admin verification.")
            return redirect('my_bookings')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('concert_detail', concert_id=concert.id)

    return render(request, 'book_ticket.html', {'concert': concert})



@login_required
def manage_concerts(request):
    bookings = C_Booking.objects.filter(status='pending').order_by('-booking_date')
    return render(request, 'manage_concerts.html', {'bookings': bookings})

@login_required
def verify_payment(request, booking_id):
    booking = get_object_or_404(C_Booking, id=booking_id)
    payment = get_object_or_404(Payment, booking=booking)

    # Mark payment as verified and confirm booking
    payment.mark_as_verified()
    
    messages.success(request, f"Payment verified for {booking.user.username}'s booking.")
    return redirect('admin_dashboard')

@login_required
def edit_concert(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)

    if request.method == 'POST':
        form = ConcertForm(request.POST, request.FILES, instance=concert)
        if form.is_valid():
            form.save()
            messages.success(request, "Concert updated successfully!")
            return redirect('admin_dashboard')
    else:
        form = ConcertForm(instance=concert)

    return render(request, 'edit_concert.html', {'form': form, 'concert': concert})
@login_required
def delete_concert(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)

    if request.method == 'POST':
        concert.delete()
        messages.success(request, "Concert deleted successfully!")
        return redirect('admin_dashboard')

    return render(request, 'delete_concert.html', {'concert': concert})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import C_Booking
from .forms import BookingUpdateForm

def update_c_booking(request, booking_id):
    booking = get_object_or_404(C_Booking, id=booking_id)

    if request.method == 'POST':
        form = BookingUpdateForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully!")
            return redirect('admin_dashboard')
    else:
        form = BookingUpdateForm(instance=booking)

    return render(request, 'update_c_booking.html', {'form': form, 'booking': booking})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contactus.html', {'form': form})
