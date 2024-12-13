import os
import time
import shutil
import pickle
import threading
import requests

from ._config import CONFIG
from ._helper import get_time
from ._models import TestLiteTestReport, TestLiteFixtureReport
from ._serializers import TestReportJSONEncoder



class fixture_after_save:
    
    def __init__(self, fixture_function, id, nodeid):
        self.fixture_function = fixture_function
        self.id = id
        self.nodeid = nodeid
        self.fixture_report = TestLiteFixtureReports.get_fixture_report(id, nodeid)


    def __call__(self, *args, **kwargs):
        with self:
            return self.fixture_function(*args, **kwargs)
        

    def __enter__(self):
        self.fixture_report.after_start_time = get_time()
        TestLiteFixtureReports.save_fixture_report(self.id, self.fixture_report)


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fixture_report.after_stop_time = get_time()
        self.fixture_report.after_status = exc_val
        TestLiteFixtureReports.save_fixture_report(self.id, self.fixture_report)



class SingletonMetaClass(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    


class TestLiteFixtureReports:

    __metaclass__ = SingletonMetaClass
    FixtureReports:dict[str, TestLiteFixtureReport] = {}


    @property
    def thr_context(self) -> dict[str, TestLiteTestReport]|dict[None]:
        if self._thr == threading.current_thread():
            return self.FixtureReports
        else:
            return {}
        

    def __init__(self):
        self._thr = threading.current_thread()


    @classmethod
    def get_all_fixtures_by_nodeid(cls, nodeid):
        return [item for item in cls.FixtureReports.values() if item.nodeid == nodeid]
        

    @classmethod    
    def get_fixture_report(cls, id: str, nodeid: str):
        '''
        id - уникальный идентификатор именно этой фикстуры для этого теста
        '''
        fixture_report = cls.FixtureReports.get(id)
        if fixture_report is None:
            return TestLiteFixtureReport(id=id, nodeid=nodeid)
        return fixture_report
    

    @classmethod
    def save_fixture_report(cls, id,  FixtureReport: TestLiteFixtureReport):
        '''
        id - уникальный идентификатор именно этой фикстуры для этого теста
        '''
        cls.FixtureReports.update({
            id: FixtureReport
        })
 


class TestLiteTestReports:

    __metaclass__ = SingletonMetaClass

    TestReports:dict[str, TestLiteTestReport] = {}
    save_pickle_file = 'TestLiteTemp'


    @property
    def thr_context(self) -> dict[str, TestLiteTestReport]|dict[None]:
        if self._thr == threading.current_thread():
            return self.TestReports
        else:
            return {}

    def __init__(self):
        self._thr = threading.current_thread()
        

    @classmethod    
    def get_test_report(cls, nodeid: str):
        test_report = cls.TestReports.get(nodeid)
        if test_report is None:
            return TestLiteTestReport(nodeid)
        return test_report
    
    @classmethod
    def save_test_report(cls, TestReport: TestLiteTestReport):
        test_report = TestReport
        test_report._fixturelist = TestLiteFixtureReports.get_all_fixtures_by_nodeid(TestReport.nodeid)
        cls.TestReports.update({
            TestReport.nodeid: test_report
        })
        


class TestLiteFinalReport:

    def __init__(self, report):
        self.report = report
        self.json_report = None

    def __call__(self) -> list[TestLiteTestReport]:
        return self.report
    
    def __repr__(self):
        return str(self.report)
    
    def __iter__(self):
        yield self.report

    @property
    def json(self):
        if self.json_report is None:
            self.json_report = TestReportJSONEncoder().encode(self.report)
        return self.json_report
    
    def save_json_file(self, file_name):
        with open(file_name, 'w') as file:
            file.write(self.json)

    def send_json_in_TestLite(self, testsuite):
        response = requests.post(
            url=f'{CONFIG().TESTLITEURL}/api/v1/project/{testsuite.split("-")[0]}/testsuite/{testsuite}/save',
            data=self.json,
            headers={
                'Content-Type': 'application/json'
            }
        )
      

class TestLiteReportManager:

    def __init__(self):
        self.reports = TestLiteTestReports().thr_context
        if not os.path.exists(CONFIG().REPORTSDIRNAME):
            os.mkdir(CONFIG().REPORTSDIRNAME)


    def save_report(self):
        match CONFIG().REPORTSSAVETYPE.upper():
            case 'TXT':
                self._save_report_as_txt_file()
            case 'BINARY':
                self._save_report_as_binary_file()


    def get_reports(self) -> TestLiteFinalReport:
        report = None
        match CONFIG().REPORTSSAVETYPE.upper():
            case 'TXT':
                report = self._read_reports_from_txt_files()
            case 'BINARY':
                report = self._read_reports_from_binary_files()
        
        if CONFIG().DELETEREPORTSDIR:
            shutil.rmtree(CONFIG().REPORTSDIRNAME)

        return TestLiteFinalReport(report)


    def _save_report_as_txt_file(self):
        with open(f'{CONFIG().REPORTSDIRNAME}/{str(threading.current_thread()).replace('<','').replace('>','')}.txt', 'w') as file:
            file.write(str(self.reports))

    
    def _save_report_as_binary_file(self):
        with open(f'{CONFIG().REPORTSDIRNAME}/{str(threading.current_thread()).replace('<','').replace('>','')}.data', 'wb') as file:
            file.write(pickle.dumps(self.reports))
    

    def _read_reports_from_binary_files(self):
        final_report = []
        listdir = os.listdir(CONFIG().REPORTSDIRNAME)
        for report_file_name in listdir:
            with open(f'{CONFIG().REPORTSDIRNAME}/{report_file_name}', 'rb') as file:
                final_report += [value for key, value in pickle.load(file).items()]
        return final_report
    
    
    def _read_reports_from_txt_files(self):
        final_report = []
        listdir = os.listdir(CONFIG().REPORTSDIRNAME)
        for report_file_name in listdir:
            with open(f'{CONFIG().REPORTSDIRNAME}/{report_file_name}', 'rb') as file:
                final_report += [value for key, value in dict(file.read()).items()]
        return final_report