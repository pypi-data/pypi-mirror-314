import sys
import os
import hashlib
import copy

from datetime import datetime

import traceback
import importlib
from tinyturret import (
    TINY_TURRET_SETTINGS,
)


def apply_global_hook():

    def tiny_turret_except_hook(exctype, value, traceback):
        sys.__excepthook__(exctype, value, traceback)

    sys.excepthook = tiny_turret_except_hook


def get_exception_group(exception, tb):
    directory, base_file_name = os.path.split(tb.tb_frame.f_code.co_filename)
    line_no = tb.tb_lineno
    exc_str = str(exception)
    exc_name = type(exception).__name__
    group_struct = {
        'exception_name': exc_name,
        'exception_message': exc_str,
        'base_file_name': base_file_name,
        'directory': directory,
        'line_number': line_no,
        'error_count': 0
    }
    group_key_str = ':'.join([
        exc_name,
        str(exception),
        str(base_file_name),
        str(line_no),
    ])
    group_key = hashlib.md5(group_key_str.encode()).hexdigest()
    return group_key, group_struct


def get_storage_backend(backend_settings):
    backend_str = backend_settings['class']
    mod_path = '.'.join(backend_str.split('.')[:-1])
    class_name = backend_str.split('.')[-1]
    somemodule = importlib.import_module(mod_path)

    bsettings = backend_settings.get('settings', {}).copy()
    default_keys = [
        'MAX_EXCEPTION_PER_GROUP', 'MAX_EXCEPTION_GROUPS'
    ]
    for setting_key in default_keys:
        if setting_key not in bsettings:
            bsettings[setting_key] = TINY_TURRET_SETTINGS[setting_key]

    return getattr(somemodule, class_name)(bsettings)


def get_locals(localz):
    if not localz:
        return localz
    out = []
    for k, v in localz.items():
        try:
            out[k] = str(v)
        except:
            pass


def serialize_exception(exception_type, exception, tbe, tb):
    directory, base_file_name = os.path.split(tb.tb_frame.f_code.co_filename)
    line_no = tb.tb_lineno
    exc_str = str(exception)
    exc_name = type(exception).__name__

    stack_trace = []
    for f in tbe.stack:
        f_no_locals = copy.deepcopy(f)
        f_no_locals.locals = None
        stack_trace.append({
            'filename': f.filename,
            'lineno': f.lineno,
            'name': f.name,
            'line': f.line,
            'end_lineno': f.end_lineno,
            'colno': f.colno,
            'end_colno': f.end_colno,
            'locals': get_locals(f.locals),
            'formatted_str': tbe.stack.format_frame_summary(f_no_locals)
        })

    exc_struct = {
        'timestamp': datetime.now().isoformat(),
        'exception_name': exc_name,
        'exception_message': exc_str,
        'base_file_name': base_file_name,
        'directory': directory,
        'line_number': line_no,
        'error_count': 0,
        'stack_trace': stack_trace,
    }
    return exc_struct


def save_exception(exception_type, exception, tbe: traceback.TracebackException, tb):
    group_key, group_struct = get_exception_group(exception, tb)
    exc_struct = serialize_exception(exception_type, exception, tbe, tb)
    for storage_backend in iter_storages():
        try:
            storage_backend.save_exception(group_key, group_struct, exc_struct)
        except Exception as e:
            if not TINY_TURRET_SETTINGS['IGNORE_STORAGE_ERRORS']:
                raise e


def get_exception_groups(top_group_count=10):
    for storage_backend in iter_storages():
        try:
            return storage_backend.get_group_list(top_group_count)
        except Exception as e:
            if not TINY_TURRET_SETTINGS['IGNORE_STORAGE_ERRORS']:
                raise e


def get_exceptions(group_key, limit=10):
    for storage_backend in iter_storages():
        try:
            return storage_backend.get_exceptions(group_key, limit)
        except Exception as e:
            if not TINY_TURRET_SETTINGS['IGNORE_STORAGE_ERRORS']:
                raise e


def iter_storages():
    for backend_settings in TINY_TURRET_SETTINGS.get('STORAGE_BACKENDS', []):
        storage_backend = get_storage_backend(backend_settings)
        yield storage_backend


def clear_storages():
    """ Clear all storage """
    for storage_backend in iter_storages():
        try:
            storage_backend.clear_db()
        except Exception as e:
            if not TINY_TURRET_SETTINGS['IGNORE_STORAGE_ERRORS']:
                raise e


def capture_exception():
    # stack_frames = traceback.extract_stack()
    value = None
    try:
        exception_type, value, tb = sys.exc_info()
        stack_frames = traceback.extract_stack(tb.tb_frame)
        tbe = traceback.TracebackException.from_exception(
            value,
            capture_locals=TINY_TURRET_SETTINGS['CAPTURE_LOCALS'],
            lookup_lines=True,
            limit=12
        )
        for f in reversed(stack_frames):
            tbe.stack.insert(0, f)
        save_exception(exception_type, value, tbe, tb)

    except Exception as e:
        if value:
            raise e from value


def register_exception_handler():
    def tinyturret_handler(exctype, value, tb):
        stack_frames = traceback.extract_stack(tb.tb_frame)[:1]
        tbe = traceback.TracebackException.from_exception(
            value,
            capture_locals=TINY_TURRET_SETTINGS['CAPTURE_LOCALS'],
            lookup_lines=True,
            limit=12
        )
        for f in reversed(stack_frames):
            tbe.stack.insert(0, f)
        save_exception(exctype, value, tbe, tb)
        sys.__excepthook__(exctype, value, tb)
    sys.excepthook = tinyturret_handler
