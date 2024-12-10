import traceback
import sys
import random
from datetime import timedelta
from django.core.exceptions import ValidationError
from simo.multimedia.controllers import BaseAudioPlayer
from .models import SonosPlayer, SonosPlaylist
from .gateways import SONOSGatewayHandler
from .forms import SONOSPlayerConfigForm


class SONOSPlayer(BaseAudioPlayer):
    gateway_class = SONOSGatewayHandler
    config_form = SONOSPlayerConfigForm

    sonos_player = None
    soco = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sonos_player = SonosPlayer.objects.filter(
            id=self.component.config.get('sonos_device')
        ).first()
        if self.sonos_player:
            self.component.sonos_player = self.sonos_player
            self.component.soco = self.sonos_player.soco
            self.soco = self.sonos_player.soco

    def unjoin(self):
        if not self.soco:
            print("NO SOCO player!", file=sys.stderr)
            return
        self.soco.unjoin()

    def _validate_val(self, val, occasion=None):
        if not self.soco:
            raise ValidationError("NO SOCO player!")
        return super()._validate_val(val, occasion)

    # LEGACY, use play_library_item instead!
    def play_playlist(self, item_id, shuffle=True, repeat=True):
        if not self.sonos_player:
            return
        for plst in self.sonos_player.soco.get_sonos_playlists():
            if plst.item_id == item_id:
                try:
                    self.soco.clear_queue()
                    self.soco.shuffle = shuffle
                    self.soco.repeat = repeat
                    self.soco.add_to_queue(plst)
                    que_size = self.soco.queue_size
                    if not que_size:
                        return
                    start_from = 0
                    if shuffle:
                        start_from = random.randint(
                            0, que_size - 1
                        )
                    self.soco.play_from_queue(start_from)
                    self.component.value = 'playing'
                    self.component.save()
                except:
                    print(traceback.format_exc(), file=sys.stderr)
                return
