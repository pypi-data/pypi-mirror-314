# -*- coding: latin -*-
from functools import wraps
from ...qt import Msg
import asyncio
from time import perf_counter
from .models import UnavailableService, InternalServerError
from fastapi import HTTPException

def _create_error(e : Exception):
    error_message = str(e)
    error_type = None
    error_code = None
    error_status_code = None

    if hasattr(e , 'message'):
        error_message = e.message
    if hasattr(e, 'type'):
        error_type = e.type
    if hasattr(e, 'code'):
        error_code = e.code
    if hasattr(e, 'status_code'):
        error_status_code = e.status_code

    return InternalServerError(message=error_message, status_code=error_status_code, type=error_type, code=error_code)

def func_router_validation(use_log = True):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if use_log:
                start = perf_counter()
            try:
                return await asyncio.create_task(func(*args, **kwargs))
            except Exception as e:
                error = _create_error(e)
                if error.status_code == 503:
                    raise HTTPException(status_code=503, detail=UnavailableService().model_dump())
                
                raise HTTPException(status_code=500, detail=error.model_dump())
            finally:
                if use_log:
                    stop = perf_counter()
                    execution_time = round(stop - start, 3)
                    print(f"The function '{func.__name__}' executed in {execution_time} seconds.")

        return wrapper

    return decorator