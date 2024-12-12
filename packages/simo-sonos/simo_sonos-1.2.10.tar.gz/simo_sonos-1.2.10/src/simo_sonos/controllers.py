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

    def play(self):
        self.soco.play()
        self.send('state_update')

    def pause(self):
        self.soco.pause()
        self.send('state_update')

    def stop(self):
        self.soco.stop()
        self.send('state_update')

    def seek(self, second):
        self.soco.seek(timedelta(seconds=second))
        self.send({'seek': second})

    def next(self):
        self.soco.next()
        self.send('state_update')

    def previous(self):
        self.soco.previous()
        self.send('state_update')

    def set_volume(self, val):
        assert 0 <= val <= 100
        self.component.soco.volume = val
        self.component.meta['volume'] = val
        self.component.save()
        self.send('state_update')

    def get_volume(self):
        return self.component.soco.volume

    def set_shuffle_play(self, val):
        self.soco.shuffle = bool(val)
        self.component.meta['shuffle'] = bool(val)
        self.component.save()
        self.send('state_update')

    def set_loop_play(self, val):
        self.soco.repeat = bool(val)
        self.component.meta['loop'] = bool(val)
        self.component.save()
        self.send('state_update')

    def play_uri(self, uri, volume=None):
        '''
        Replace que with this single uri and play it immediately
        :param uri: playable uri or url
        :param volume: volume at which to play
        :return:
        '''
        if volume:
            assert 0 <= volume <= 100
            self.set_volume(volume)
        self.soco.play_uri(uri)
        self.send('state_update')

    def play_library_item(self, id, volume=None, fade_in=None):
        '''
        :param id: Library item ID
        :param volume: Volume to play at. Current volume will be used if not provided
        :param fade_in: number of seconds to fade in
        :return:
        '''
        try:
            SonosPlaylist.objects.get(
                id=id, player_id=self.component.config['sonos_device']
            )
        except SonosPlaylist.DoesNotExist:
            raise Exception("Media item does not exist on this on this player!")
        self.send({'play_from_library': id, 'volume': volume, 'fade_in': fade_in})

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
