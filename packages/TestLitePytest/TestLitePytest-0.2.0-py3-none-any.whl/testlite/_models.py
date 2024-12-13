import re

from datetime import datetime
from enum import Enum
from dataclasses import dataclass



class STATUS(str, Enum):
    SKIP = 'skip'
    PASSED = 'passed'
    FAIL = 'fail'
    ERROR = 'error'



@dataclass
class FixtureRunResult:
    result: str = None # Что возвращает фикстура
    status: STATUS = None
    error: str = None



@dataclass
class TestLiteFixtureReport:
    id: str
    nodeid: str 
    name: str = None
    cached_result: tuple = None
    before_start_time: float = None
    before_stop_time: float = None
    after_start_time: float = None
    after_stop_time: float = None
    _after_error = None


    @property
    def before_duration(self):
        if self.before_stop_time is not None:
            return self.before_stop_time - self.before_start_time
        else:
            return 0 - self.before_start_time
    

    @property
    def after_duration(self):
        if self.after_stop_time is not None and self.after_start_time is not None:
            return self.after_stop_time - self.after_start_time
        else:
            return None
        

    @property
    def before_status(self):
        if self.cached_result[2] is None:
            return FixtureRunResult(
                result=self.cached_result[0],
                status=STATUS.PASSED
            )
        else:
            return FixtureRunResult(
                status=STATUS.ERROR,
                error=self.cached_result[2]
            )
    

    @property
    def after_status(self):
        return self._after_error
    

    @after_status.setter
    def after_status(self, exc_val):
        if exc_val is not None:
            self._after_error = FixtureRunResult(
                status=STATUS.ERROR,
                error=exc_val
            )
        else:
            self._after_error = FixtureRunResult(
                status=STATUS.PASSED
            )



@dataclass
class TestLiteTestReport:
    nodeid: str
    testcase_key: str = None
    status: str = None
    startime_timestamp: float = None
    stoptime_timestamp: float = None
    report: str = None
    log: str = None
    params: str = None
    skipreason: str = None
    precondition_status: str = None
    postcondition_status: str = None
    step_number_with_error: int = None

    _fixturelist: list[TestLiteFixtureReport] = None


    @property
    def parametrize_name(self):
        name = re.search('\[.*\]', self.nodeid)
        if name is None:
            return None
        else:
            return name[0]


    @property
    def duration(self):
        if self.stoptime_timestamp is not None:
            return round(self.stoptime_timestamp - self.startime_timestamp, 2)
        else:
            return None


    @property    
    def startime_readable(self):
        if self.startime_timestamp is not None:
            return datetime.fromtimestamp(self.startime_timestamp)
        else:
            return None
        
    @property
    def stoptime_readable(self):
        if self.stoptime_timestamp is not None:
            return datetime.fromtimestamp(self.stoptime_timestamp)
        else:
            return None
        

    @property
    def fixtures(self):
        fixture_dict = {
            'before': [],
            'after': []
        }
        fixtures = self._fixturelist
        for fixture in fixtures:
            fixture_dict['before'].append(fixture)
            if fixture.after_duration is not None:
                fixture_dict['after'].append(fixture)
        return fixture_dict
    

    def add_log(self, log):
        self.log = self.log + log
