import json
import traceback

from dataclasses import asdict

from ._models import TestLiteTestReport, FixtureRunResult, TestLiteFixtureReport


class MakeDict:

    def __init__(self):
        self.remake_object = None


    def _make_dict_from_FixtureRunResult(self, obj):
        if isinstance(obj, FixtureRunResult):
            item = asdict(obj)
            item.update({
                'error': "".join(traceback.format_exception_only(type(obj.error), obj.error)).strip() if obj.error is not None else None
            })
            return item
        else:
            raise Exception('Its not a FixtureRunResult clas')
    

    def remake(self, obj, key):
        if isinstance(obj, TestLiteFixtureReport):
            item = {}
            if key == 'before':
                item.update({
                    'name': obj.name,
                    'start_time': obj.before_start_time,
                    'stop_time': obj.before_stop_time,
                    'duration': obj.before_duration,
                    'status': self._make_dict_from_FixtureRunResult(obj.before_status)
                })
            if key == 'after':
                item.update({
                    'name': obj.name,
                    'start_time': obj.after_start_time,
                    'stop_time': obj.after_stop_time,
                    'duration': obj.after_duration,
                    'status': self._make_dict_from_FixtureRunResult(obj.after_status)
                })
            return item
        else:
            raise Exception('Its not TestLiteFixtureReport class')
        

    def make_serializable_dict_from_fixtures_dict(self, fixtures_dict):
        self.remake_object = fixtures_dict
        if isinstance(self.remake_object, dict):
            for key, value in self.remake_object.items():
                for i, item in enumerate(value):
                    self.remake_object[key][i] = self.remake(item, key)
            return self.remake_object
        else:
            raise Exception('Its not a dict')



class TestReportJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, TestLiteTestReport):
            item = asdict(o)
            item.update({
                'parametrize_name': str(o.parametrize_name),
                'startime_readable': str(o.startime_readable),
                'stoptime_readable': str(o.stoptime_readable), 
                'duration': float(o.duration),
                'duration': float(o.duration),
                'fixtures': MakeDict().make_serializable_dict_from_fixtures_dict(o.fixtures)
            })
            return item
        return super().default(o)