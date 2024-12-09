
def TestLite_testcase_key(item):
    return getattr(
        getattr(item, "obj", None),
        "__TestLite_testcase_key__",
        None
    )


def get_step_number_with_error(longreprtext: str) -> int|None:
    step_number = 0
    for i, line in enumerate(longreprtext.split('\n')):
        print(f'{i}: {line}')
        if '#TestLiteStep' in line:
            step_number += 1
    return step_number if step_number !=0 else None

