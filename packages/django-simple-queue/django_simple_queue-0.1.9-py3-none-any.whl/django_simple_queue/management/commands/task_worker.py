import asyncio

from django.core.management.base import BaseCommand
from django_simple_queue.models import Task
from django.utils import timezone
import importlib
import time
import json
import inspect
import random
import traceback


def process_task(task_id):
    task_obj = Task.objects.get(id=task_id)
    print(f"Initiating task id: {task_id}")
    if task_obj.status == Task.QUEUED:  # One more extra check to make sure
        try:
            path = task_obj.task.split('.')
            module = importlib.import_module('.'.join(path[:-1]))
            func = getattr(module, path[-1])
            args = json.loads(task_obj.args)
            task_obj.output = ""
            task_obj.status = Task.PROGRESS
            task_obj.save()

            # In case event loop gets killed
            try:
                asyncio.set_event_loop(asyncio.get_running_loop())
            except RuntimeError:
                asyncio.set_event_loop(asyncio.new_event_loop())

            if inspect.isgeneratorfunction(func):
                for i in func(**args):
                    output = i
                    task_obj.output += output
                    task_obj.save()
            else:
                task_obj.output = func(**args)
                task_obj.save()
            task_obj.status = Task.COMPLETED
            task_obj.save()
        except Exception as e:
            task_obj.output += f"{repr(e)}\n\n{traceback.format_exc()}"
            task_obj.status = Task.FAILED
            task_obj.save()
        finally:
            print(f"Finished task id: {task_id}")


class Command(BaseCommand):
    help = 'Executes the enqueued tasks.'

    def handle(self, *args, **options):
        try:
            sleep_interval = random.randint(3, 9)
            while True:
                time.sleep(sleep_interval)
                print(f"{timezone.now()}: Heartbeat..")
                queued_task = Task.objects.filter(status=Task.QUEUED).order_by('modified').first()
                if queued_task:
                    process_task(task_id=queued_task.id)
        except KeyboardInterrupt:
            pass
