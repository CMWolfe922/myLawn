from django.forms import ModelForm
from django import forms
from .models import Place, Lawn, Booking, Review

class PlaceForm(ModelForm):

    # get the longitude and latitude from the users
    # address input and save it to the location field
    address = forms.CharField(max_length=100)

    def save(self, commit=True):
        place = super().save(commit=False)
        place.location = self.cleaned_data['address']
        if commit:
            place.save()
        return place
    class Meta:
        model = Place
        fields = ['name', 'location']


class LawnForm(ModelForm):
    class Meta:
        model = Lawn
        fields = '__all__'


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        oredering = ['date', 'start_time', 'end_time']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        ordering = ['rating', 'comment']
