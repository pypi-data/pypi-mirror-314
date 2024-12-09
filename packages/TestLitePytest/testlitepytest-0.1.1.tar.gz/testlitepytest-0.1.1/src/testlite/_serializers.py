import json
from dataclasses import asdict

from TestLite._models import TestLiteTestReport


class TestReportJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, TestLiteTestReport):
            item = asdict(o)
            item.update({
                'startime_readable': str(o.startime_readable),
                'stoptime_readable': str(o.stoptime_readable), 
                'duration': float(o.duration)
            })
            return item
        return super().default(o)