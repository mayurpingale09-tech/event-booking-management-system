from django import forms
from .models import Event, EVENT_CATEGORIES

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'price', 'image']
    
    # We specify the choices manually for the 'category' field since it's a CharField with choices.
    category = forms.ChoiceField(choices=EVENT_CATEGORIES, required=True)


from django import forms
from .models import Concert

class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ['name', 'description', 'date', 'venue', 'address', 'city', 'state', 'country', 
                  'ticket_price', 'total_tickets', 'available_tickets', 'qr_code', 'image']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

from django import forms
from .models import C_Booking

class BookingUpdateForm(forms.ModelForm):
    class Meta:
        model = C_Booking
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')], attrs={'class': 'form-control'})
        }

from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 4}),
        }
