from django import forms
from . models import Encoding, Decoding

class EncodeForm(forms.ModelForm):
    class Meta:
        model = Encoding
        fields = ['file','frame_number', 'secret_key', 'message',]


class DecodeForm(forms.ModelForm):
    class Meta:
        model = Decoding
        fields = ['file','frame_number', 'secret_key']
