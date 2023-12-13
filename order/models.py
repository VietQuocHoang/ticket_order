from datetime import datetime

from django.db import models


# Create your models here.
class TicketManager(models.Manager):
    pass


class Ticket(models.Model):
    token = models.UUIDField(null=False, blank=False)
    objects = TicketManager()


class TicketRegeneratingStatusManager(models.Manager):
    pass

class TicketRegeneratingStatus(models.Model):
    ticket_id = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField(default=datetime.now)
    objects = TicketRegeneratingStatusManager()
