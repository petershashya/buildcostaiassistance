from django import forms
from .models import HouseMap


class HouseMapForm(forms.ModelForm):
    class Meta:
        model = HouseMap
        fields = ['map_image']
        labels = {
            'map_image': 'House Map',
        }