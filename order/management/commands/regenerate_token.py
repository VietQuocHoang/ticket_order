import time

from datetime import datetime
from uuid import uuid4

from memory_profiler import profile

from django.core.management.base import BaseCommand
from order.models import Ticket, TicketRegeneratingStatus


class Command(BaseCommand):
    help = "Regenerating the token for all ticket order"

    def add_arguments(self, parser):
        parser.add_argument(
            "--iterator",
            nargs="?",
            type=int,
            default=1,
            help="Default 1, Passing --iterator=0 to disable using iterator to regenerate the token for order ticket, will consume more memory",
        )
        parser.add_argument(
            "--bulk",
            nargs="?",
            type=int,
            default=0,
            help="Default 0, Passing --bulk=1 to using bulk_create, enabling this option will have no resuming regenerate feature but significantly improve the time execution",
        )

    @profile(precision=4)
    def handle(self, *args, **kwargs):
        self.stdout.write("Starting generating ")
        starttime = time.time()
        queryset = Ticket.objects

        # Get the last execution progress
        if TicketRegeneratingStatus.objects.exists():
            status = TicketRegeneratingStatus.objects.first()
            queryset = queryset.filter(id__gte=status.ticket_id)
            self.stdout.write(f"Resuming from {status.ticket_id}")
        else:
            status = TicketRegeneratingStatus.objects.create()

        queryset = queryset.order_by("id").all()

        max_iter = queryset.count()

        if kwargs.get("iterator", 1) == 1:
            queryset = queryset.iterator(chunk_size=10000)

        bulk = kwargs.get("bulk", 0)
        curr_iter = 1
        for object in queryset:
            new_uuid = uuid4()
            object.token = new_uuid
            if bulk == 0:
                self.stdout.write()
                object.save()
                status.ticket_id = object.id
                status.save()

            time_elapsed, left_time, finish_time = self.calculate_elapse_time(
                starttime=starttime, curr_iter=curr_iter, max_iter=max_iter
            )
            self.stdout.write(
                f"Item id: {object.id} Elapsed time: {time_elapsed}(s), ETA time left: {left_time}(s), ETA Finish Time: {finish_time} UTC",
                ending="\r",
            )
            curr_iter += 1

        if bulk == 1:
            self.stdout.write("Performing bulk updating")
            Ticket.objects.bulk_update(queryset, fields=["token"])

        # Clear out the status table 
        status.delete()

    def calculate_elapse_time(self, starttime, curr_iter, max_iter):
        telapsed = time.time() - starttime
        testimated = (telapsed / curr_iter) * (max_iter)

        finishtime = starttime + testimated
        finishtime = datetime.fromtimestamp(finishtime).strftime("%H:%M:%S")  # in time

        lefttime = testimated - telapsed  # in seconds

        return (int(telapsed), int(lefttime), finishtime)
