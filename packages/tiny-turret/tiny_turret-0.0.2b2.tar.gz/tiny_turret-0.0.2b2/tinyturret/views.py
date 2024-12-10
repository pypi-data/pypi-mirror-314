from django.contrib import admin, messages
from django.shortcuts import redirect, render

import pickle

from tinyturret.utils import get_exception_groups, get_exceptions


def main_turret_view(request):
    context_data = {
        **admin.site.each_context(request),
        'exception_groups': get_exception_groups()
    }
    return render(request, 'tinyturret/main.html', context_data)


def exception_views(request, group_key):
    exception_list = get_exceptions(group_key, limit=request.GET.get('limit', 10))
    context_data = {
        **admin.site.each_context(request),
        'exceptions': exception_list
    }
    return render(request, 'tinyturret/exception.html', context_data)
