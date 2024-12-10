from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from dirtyfields import DirtyFieldsMixin
from soco import SoCo


class SonosPlayer(DirtyFieldsMixin, models.Model):
    slave_of = models.ForeignKey(
        'SonosPlayer', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='slaves'
    )
    uid = models.CharField(max_length=200, db_index=True, unique=True)
    name = models.CharField(max_length=200, db_index=True)
    ip = models.GenericIPAddressField()
    last_seen = models.DateTimeField(auto_now_add=True)
    is_alive = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.soco = SoCo(self.ip)

    def __str__(self):
        return f'{self.name} ({self.uid}) '


@receiver(post_save, sender=SonosPlayer)
def update_related_components(sender, instance, created, **kwargs):
    if created:
        return
    if 'is_alive' not in instance.get_dirty_fields():
        return
    from simo_sonos.gateways import SONOSGatewayHandler
    from simo.core.models import Component
    for component in Component.objects.filter(
        gateway__type=SONOSGatewayHandler.uid, base_type='audio-player',
    ):
        if component.config.get('sonos_device') != instance.id:
            continue
        component.alive = instance.is_alive
        component.save()


class SonosPlaylist(models.Model):
    player = models.ForeignKey(SonosPlayer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    item_id = models.CharField(max_length=200)

    class Meta:
        unique_together = 'player', 'item_id'

    def __str__(self):
        return f"{self.title} on {self.player}"
