from django import forms
from .models import Booking
from .utils import get_available_slots

class PublicBookingForm(forms.ModelForm):
    full_name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    slot = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slot'].choices = [
            (slot["datetime"].isoformat(), slot["label"])
            for slot in get_available_slots()
        ]

    class Meta:
        model = Booking
        fields = ['address', 'zip_code', 'notes']
