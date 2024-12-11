import contextlib

if not hasattr(contextlib, "nullcontext"):

    class nullcontext(contextlib.AbstractContextManager):
        def __init__(self, enter_result=None):
            self.enter_result = enter_result

        def __enter__(self):
            return self.enter_result

        def __exit__(self, *excinfo):
            pass
else:
    nullcontext = contextlib.nullcontext
