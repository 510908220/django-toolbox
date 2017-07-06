import json
import datetime

from picklefield import PickledObjectField

from django.shortcuts import render
from django.http import HttpResponse
from django_q.tasks import Async
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


def task(request):
    if request.method == 'GET':
        tasks = list(Task.objects.values('id', 'name', 'started', 'stopped', 'result'))
        return HttpResponse(json.dumps(tasks,  cls=CJsonEncoder), content_type="application/json")
    elif request.method == 'POST':
        num = request.POST.get('num')
        opts = {'task_name': 'fib' + str(num),
                'group': 'fib'}
        #Async('xxx.tasks.fib', num, q_options=opts).run()
        return HttpResponse(opts, content_type="application/json")


def schedule(request):
    if request.method == 'GET':
        schedules = list(Schedule.objects.values('name', 'schedule_type', 'next_run'))
        return HttpResponse(json.dumps(schedules,  cls=CJsonEncoder), content_type="application/json")
    elif request.method == 'POST':
        return HttpResponse({'foo': 'bar'}, content_type="application/json")
