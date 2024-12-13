
def test_key(TestLite_id):

    def decorator(func):
        if getattr(func, '__pytest_wrapped__', None):
            function = func.__pytest_wrapped__.obj
        else:
            function = func
        function.__TestLite_testcase_key__ = TestLite_id
        return func
    
    return decorator

