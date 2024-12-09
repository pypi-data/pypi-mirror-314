import pytest
from testlite._reports import TestLiteTestReports as TRs
from testlite._reports import TestLiteTestReport as TR
from testlite._reports import TestLiteReportManager
from testlite._models import STATUS
from testlite._Testlite import TestLite_testcase_key, get_step_number_with_error


def pytest_addoption(parser):
    group = parser.getgroup('TestLitePytest')
    group.addoption(
        '--testsuite',
        action='store',
        dest='testsuite',
        help='Set TestSuite Key. If the option is specified, then at the end we will try to send the results to TestLite'
    )
    group.addoption(
        '--save_json',
        action='store',
        dest='savejson',
        default=None,
        help='After end of testing saving JSON file with report'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')



def pytest_configure(config):
    config.TSTestReports = TRs()



# def pytest_addoption(parser: pytest.Parser):
#     parser.addoption('--testsuite', action='store')
#     parser.addoption('--save_json', action='store', default=None)



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report: pytest.TestReport = outcome.get_result()
    test_report: TR = item.config.TSTestReports.get_test_report(report.nodeid)
    test_report.testcase_key = TestLite_testcase_key(item)


    if report.when == 'setup':
        if report.skipped == True:
            test_report.status = STATUS.SKIP
            test_report.skipreason = report.longrepr[2]

            test_report.startime_timestamp = report.start
            test_report.stoptime_timestamp = report.stop


        if report.failed == True:
            test_report.precondition_status = STATUS.ERROR
            test_report.status = STATUS.ERROR
            test_report.report = report.longreprtext

            test_report.startime_timestamp = report.start
            test_report.stoptime_timestamp = report.stop


        if report.passed == True:
            test_report.precondition_status = STATUS.PASSED

            test_report.startime_timestamp = report.start


    if test_report.status != STATUS.SKIP and report.when == 'call':
        if report.passed == True:
            test_report.status = STATUS.PASSED


        if report.failed == True:
            test_report.step_number_with_error = get_step_number_with_error(report.longreprtext)
            test_report.status = STATUS.FAIL
            test_report.report = report.longreprtext


    if test_report.status != STATUS.SKIP and report.when == 'teardown':
        if report.failed == True:
            test_report.postcondition_status = STATUS.ERROR
            test_report.report = report.longreprtext
        if report.passed == True:
            test_report.postcondition_status = STATUS.PASSED

        test_report.log = report.caplog
        test_report.stoptime_timestamp = report.stop

    item.config.TSTestReports.save_test_report(test_report)  


def pytest_sessionfinish(session: pytest.Session, exitstatus):
    if hasattr(session.config, "workerinput"):
        TestLiteReportManager().save_report()
    else:
        TestLiteReportManager().save_report()
        final_report = TestLiteReportManager().get_reports()
        if session.config.getoption('--save_json') is not None:
            final_report.save_json_file(session.config.getoption("--save_json"))
        if session.config.getoption('--testsuite'):
            final_report.send_json_in_TestLite(testsuite=session.config.getoption('--testsuite'))
