import os
import shutil
import pickle
import threading
import requests

from ._config import CONFIG
from ._models import TestLiteTestReport
from ._serializers import TestReportJSONEncoder



class TestLiteTestReportsMetaClass(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
 

class TestLiteTestReports:
    # Ебани сюда пикл и проверь, а потом еще добавь хуету чтобы вконце все потоки соединили свою хуету в одну хуету
    __metaclass__ = TestLiteTestReportsMetaClass

    TestReports:dict[str, TestLiteTestReport] = {}
    save_pickle_file = 'TestLiteTemp'
    # thread_list = []


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
        cls.TestReports.update({
            TestReport.nodeid: TestReport
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
            url=f'{CONFIG.TESTLITEURL}/api/v1/project/{testsuite.split("-")[0]}/testsuite/{testsuite}/save',
            data=self.json,
            headers={
                'Content-Type': 'application/json'
            }
        )
      

class TestLiteReportManager:

    def __init__(self):
        self.reports = TestLiteTestReports().thr_context
        if not os.path.exists(CONFIG.REPORTSDIRNAME):
            os.mkdir(CONFIG.REPORTSDIRNAME)


    def save_report(self):
        match CONFIG.REPORTSSAVETYPE.upper():
            case 'TXT':
                self._save_report_as_txt_file()
            case 'BINARY':
                self._save_report_as_binary_file()


    def get_reports(self) -> TestLiteFinalReport:
        report = None
        match CONFIG.REPORTSSAVETYPE.upper():
            case 'TXT':
                report = self._read_reports_from_txt_files()
            case 'BINARY':
                report = self._read_reports_from_binary_files()
        
        if CONFIG.DELETEREPORTSDIR:
            shutil.rmtree(CONFIG.REPORTSDIRNAME)

        return TestLiteFinalReport(report)


    def _save_report_as_txt_file(self):
        with open(f'{CONFIG.REPORTSDIRNAME}/{str(threading.current_thread()).replace('<','').replace('>','')}.txt', 'w') as file:
            file.write(str(self.reports))

    
    def _save_report_as_binary_file(self):
        with open(f'{CONFIG.REPORTSDIRNAME}/{str(threading.current_thread()).replace('<','').replace('>','')}.data', 'wb') as file:
            file.write(pickle.dumps(self.reports))
    

    def _read_reports_from_binary_files(self):
        final_report = []
        listdir = os.listdir(CONFIG.REPORTSDIRNAME)
        for report_file_name in listdir:
            with open(f'{CONFIG.REPORTSDIRNAME}/{report_file_name}', 'rb') as file:
                final_report += [value for key, value in pickle.load(file).items()]
        return final_report
    
    
    def _read_reports_from_txt_files(self):
        final_report = []
        listdir = os.listdir(CONFIG.REPORTSDIRNAME)
        for report_file_name in listdir:
            with open(f'{CONFIG.REPORTSDIRNAME}/{report_file_name}', 'rb') as file:
                final_report += [value for key, value in dict(file.read()).items()]
        return final_report