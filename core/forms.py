from django import forms
from . models import Encoding

class EncodeForm(forms.ModelForm):
    class Meta:
        model = Encoding
        fields = ['file','frame_number', 'secret_key', 'message',]