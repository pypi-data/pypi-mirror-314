from django import forms
from simo.core.forms import BaseComponentForm
from .models import SonosPlayer, SonosPlaylist


class SONOSPlayerConfigForm(BaseComponentForm):
    sonos_device = forms.ModelChoiceField(
        queryset=SonosPlayer.objects.all()
    )
