from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel

from komora_service_path_plugin.models import Segment
from komora_service_path_plugin.models.sync_status_choices import SyncStatusChoices


class ServicePath(NetBoxModel):
    name = models.CharField(max_length=225)
    state = models.CharField(
        max_length=225
    )  # TODO: maybe choice field? Or extra table? (I don't like extra table)
    kind = models.CharField(
        max_length=225
    )  # TODO: maybe choice field? Or extra table? (I don't like extra table)
    sync_status = models.CharField(
        max_length=30,
        choices=SyncStatusChoices,
        blank=False,
        default="active",
    )

    segments = models.ManyToManyField(Segment, through="ServicePathSegmentMapping")

    # Komora fields
    imported_data = models.JSONField(null=True, blank=True)
    komora_id = models.BigIntegerField(null=True, blank=True)  # TODO: change to False

    comments = models.TextField(verbose_name="Comments", blank=True)

    class Meta:
        ordering = ("name", "state", "kind")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:komora_service_path_plugin:servicepath", args=[self.pk])

    def get_sync_status_color(self):
        return SyncStatusChoices.colors.get(self.sync_status)
