from pathlib import Path
import os

# Constants
FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]


OPERATORS_REGISTRY = {}

def operator_register(*args):
   
    key_list = [arg for arg in args]

    def decorator(operator):
        class Wrapper(operator):
            def __init__(self, *args, **kwargs):
                return operator(*args, **kwargs)
        
        for key in key_list:
            OPERATORS_REGISTRY[key] = operator

        return Wrapper
    return decorator

def supported_operators():
    return list(OPERATORS_REGISTRY.keys())
