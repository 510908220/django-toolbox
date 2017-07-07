import json
import datetime
import random

from picklefield import PickledObjectField

from django.shortcuts import render
from django.http import HttpResponse
from django_q.tasks import Async, schedule
from django_q.models import Schedule, Task
# Create your views here.


class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


def index(request):
    return render(request, 'xxx/index.html', {})


def task_handler(request):
    if request.method == 'GET':
        tasks = list(Task.objects.values('id', 'name', 'started', 'stopped', 'result', 'group'))
        return HttpResponse(json.dumps(tasks,  cls=CJsonEncoder), content_type="application/json")
    elif request.method == 'POST':
        num = json.loads(str(request.body, 'utf-8')).get('num')
        opts = {'task_name': 'fib' + str(num),
                'group': 'fib'}

        task_id = Async('xxx.tasks.fib', int(num), q_options=opts).run()
        return HttpResponse({"task_id": task_id}, content_type="application/json")


def schedule_handler(request):
    if request.method == 'GET':
        schedules = list(Schedule.objects.values('name', 'schedule_type', 'next_run'))
        return HttpResponse(json.dumps(schedules,  cls=CJsonEncoder), content_type="application/json")
    elif request.method == 'POST':
        data = json.loads(str(request.body, 'utf-8'))
        schedule_type = data.get('schedule_type')
        name = data.get('name')

        schedule('xxx.tasks.fib', random.randint(1, 38),
                 name=name,
                 schedule_type=schedule_type,
                 q_options={
                     'task_name': 'xxx',
                     'timeout': 60}
                 )
        return HttpResponse({'name': name}, content_type="application/json")
