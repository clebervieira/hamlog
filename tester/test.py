
import os
import sys
import logging
import traceback
from fnmatch import fnmatch

from .port_manager import portManager


_logger = logging.getLogger(__name__)


class HarnessTest(object):

    def classSetUp(self, dockerImage = None):
        self.net = None
        self.testCasesRun = 0
        self.testCasesPassed = 0
        self.testCasesFailed = []
        self.testCasesSkipped = []
        self.cleanupAfter = True    # Set this to False to leave folders in /tmp
        self.leaveRunning = False   # Set this to True to wait for Ctrl-C before tearing down test
        self.aborted = False
        self.dockerImage = dockerImage
        self.portManager = portManager()
        self.suiteSetUp()

    def classTearDown(self):
        self.suiteTearDown()

    def _getTestMethods(self, methodPattern):
        result = []
        for m in dir(self):
            method = getattr(self, m)
            if callable(method) and m.startswith('test_') and fnmatch(m, methodPattern):
                result.append(method)
        return result

    def run(self, methodPattern = '*', continueAfterFailure = True, ignoreSkips = False, iterations = 1):
        _logger.info("Starting test class '{}' with test case pattern '{}'...".format(type(self).__name__, methodPattern))
        for testMethod in self._getTestMethods(methodPattern):
            if not ignoreSkips and testMethod.__doc__ and "skip" in testMethod.__doc__.lower():
                self.testCasesSkipped.append(testMethod.__name__)
                continue
            self.testCasesRun += 1
            if self._runTestMethod(testMethod, iterations):
                self.testCasesPassed += 1
            else:
                self.testCasesFailed.append(testMethod.__name__)
                if not continueAfterFailure:
                    self.aborted = True
                    break

        _logger.info("Ran {} test cases from test class '{}':  {} passed.".format(self.testCasesRun, type(self).__name__, self.testCasesPassed))

    def _runTestMethod(self, testMethod, iterations):
        for iteration in range(iterations):
            self.cleanupAfter = True
            failed = False
            msg = "- running {}...".format(testMethod.__name__)
            if iterations > 1:
                msg += (" ({}/{})".format(1 + iteration, iterations))
            _logger.info(msg)
            try:
                self.testSetUp()
                testMethod()
                self.checkForReportedErrors()
                _logger.info(" " * len(msg) + "PASS.")
            except AssertionError as e:
                lineno = None
                assertFrame = sys.exc_info()[2]
                while assertFrame:
                    filename = assertFrame.tb_frame.f_code.co_filename
                    lineno = assertFrame.tb_frame.f_lineno
                    assertFrame = assertFrame.tb_next
                del assertFrame
                assertLoc = "  ({}:{})".format(filename.split('/')[-1], lineno) if lineno else ""
                if _logger.level <= logging.INFO:
                    _logger.info("- " + " " * (len(msg) - 2) + "FAIL!" + assertLoc)
                else:
                    _logger.error("FAIL:  test case '{}' in class '{}'".format(lineno, testMethod.__name__, type(self).__name__) + assertLoc)
                failed = True
            except (Exception, KeyboardInterrupt) as e:
                _logger.error("Exception running test '{}' in class '{}':  {}".format(testMethod.__name__, type(self).__name__,  e if not isinstance(e, KeyboardInterrupt) else "KeyboardInterrupt"))
                _logger.error("VVVV stack trace was:  VVVV")
                traceback.print_tb(sys.exc_info()[2])
                _logger.error("^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                _logger.error("FAIL:  test case '{}' in class '{}'".format(testMethod.__name__, type(self).__name__))
                failed = True
                if isinstance(e, KeyboardInterrupt):
                    continueAfterFailure = False

            if failed:
                if iteration > 0:
                    _logger.error("   [ FAIL was on iteration {}/{} ]".format(1 + iteration, iterations))
                self.cleanupAfter = False

            if not self.cleanupAfter:
                _logger.warn("Test class '{}' not cleaning up test remnants for test '{}'.".format(type(self).__name__, testMethod.__name__))
                self.logTestRemnants()
            if self.leaveRunning:
                self.waitForCtrlC()
            try:
                self.testTearDown()
            except Exception as e:
                _logger.error("    Test {} teardown failure: {}".format(testMethod.__name__, e))
                raise e
            if failed:
                return False
        return True

    def waitForCtrlC(self):
        try:
            msg = '\n' + (self.testLeaveRunningStatus() or '')
            msg += "\n\n   *** Leaving network running until Ctrl-C is hit... ***\n"
            _logger.warn(msg)
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            pass


    ## test helpers

    def assertRaisesException(self, closure, msgExpect = None):
        try:
            closure()
        except Exception as e:
            if msgExpect:
                if hasattr(e, 'output'):
                    # for handling CalledProcess exceptions
                    excStr = e.output
                else:
                    excStr = str(e)
                if -1 == excStr.lower().find(msgExpect):
                    raise Exception("Exception raised, but '{}' not found in '{}'".format(msgExpect, e.output))
            return e
        raise Exception("Did not fail as expected")


    ## overrides

    def suiteSetUp(self):
        pass

    def suiteTearDown(self):
        pass

    def testSetUp(self):
        ASSERT_OVERRIDE_REQUIRED

    def testTearDown(self):
        ASSERT_OVERRIDE_REQUIRED

    def checkForReportedErrors(self):
        ASSERT_OVERRIDE_REQUIRED

    def logTestRemnants(self):
        ASSERT_OVERRIDE_REQUIRED

    def testLeaveRunningStatus(self):
        ASSERT_OVERRIDE_REQUIRED
