from datetime import datetime
from enum import Enum
from dataclasses import dataclass



class STATUS(str, Enum):
    SKIP = 'skip'
    PASSED = 'passed'
    FAIL = 'fail'
    ERROR = 'error'


@dataclass
class TestLiteTestReport:
    nodeid: str
    testcase_key: str = None
    status: str = None
    startime_timestamp: float = None
    stoptime_timestamp: float = None
    # duration: float = None
    report: str = None
    log: str = None
    skipreason: str = None
    precondition_status: str = None
    postcondition_status: str = None
    step_number_with_error: int = None


    @property
    def duration(self):
        if self.stoptime_timestamp is not None:
            return round(self.stoptime_timestamp - self.startime_timestamp, 2)
            # return f'{(self.stoptime_timestamp - self.startime_timestamp):.2f}'
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
    
    def add_log(self, log):
        self.log = self.log + log
