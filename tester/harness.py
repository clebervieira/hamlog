import logging
from pkgutil import iter_modules
from importlib import import_module
from inspect import isclass
from fnmatch import fnmatch

from .test import HarnessTest

_logger = logging.getLogger(__name__)


class Harness(object):

    def __init__(self, args):
        self._continue = True
        self._dockerImage = None
        self._aborted = False
        self._ignoreSkips = False
        self._leaveRunning = False
        self._packageName = None
        self._iterations = 1
        self.testClassesRun = 0
        self.testCasesRun = 0
        self.testCasesPassed = 0
        self.testCasesFailed = []
        self.testCasesSkipped = []
        self._testPatterns = []
        self._parseArgs(args)

    def _parseArgs(self, args):
        for testpat in args:
            if testpat == "--continue":
                self._continue = True
                _logger.info("Tester will try to continue after failed tests.")
                continue
            elif testpat == "--abort":
                self._continue = False
                _logger.info("Tester will abort after failed tests.")
                continue
            elif testpat == "--ignore-skip":
                self._ignoreSkips = True
                _logger.info("Tester will ignore 'skip' markers in test docstrings.")
                continue
            elif testpat == "--leave-running":
                self._leaveRunning = True
                _logger.info("Tester will leave tests running after a failure.")
                continue
            elif testpat.startswith("--iterations="):
                self._iterations = int(testpat.split('=')[1])
            elif testpat.startswith("--pkg="):
                self._packageName = testpat.split('=')[1]
            elif testpat.startswith("--docker="):
                ASSERT_NYI
                self._dockerImage = testpat.split('=')[-1]
                _logger.info("Tester will use docker image '{}'.".format(self._dockerImage))
                continue
            parts = testpat.split('.')
            if len(parts) > 3:
                raise Exception("ill-formed path to tests: must have no more than 3 components")
            self._testPatterns.append(testpat)

    def _runTestPattern(self, testPat):
        if testPat in ['all', '*', '*.*']:
            testPat = '*.*.*'
        mypkg = (self._packageName or __package__) + ".tests"
        mypkgMod = import_module(mypkg)
        parts = testPat.split('.')
        modules = []
        for _, modname, _ in iter_modules(mypkgMod.__path__):
            if fnmatch(modname, parts[0]):
                modules.append(import_module('.' + modname, mypkg))
        methodPattern = parts[2] if len(parts) > 2 else '*'
        for module in modules:
            for c in dir(module):
                klass = getattr(module, c)
                if isclass(klass) and issubclass(klass, HarnessTest) and (len(parts) < 2 or fnmatch(c, parts[1])):
                    if klass().__class__.__module__.startswith(mypkg):    # necessary to skip imported classes
                        self._runClassTests(klass, methodPattern)
                        if self._aborted:
                            return

    def _runClassTests(self, testclass, methodPattern):
        test = testclass()
        test.classSetUp(dockerImage=self._dockerImage)
        if self._leaveRunning:
            test.leaveRunning = True
        test.run(methodPattern, self._continue, self._ignoreSkips, self._iterations)
        self._aborted = test.aborted
        self.testClassesRun += 1
        self.testCasesRun += test.testCasesRun
        self.testCasesPassed += test.testCasesPassed
        self.testCasesFailed += test.testCasesFailed
        self.testCasesSkipped += test.testCasesSkipped
        test.classTearDown()

    def run(self):
        ok = True
        for testpat in self._testPatterns:
             self._runTestPattern(testpat)
             if self._aborted:
                 _logger.info("Tester:  aborted testing.")
                 ok = False
                 break
        _logger.info("Tester SUMMARY:  Passed {} of {} total test cases from {} test classes.".format(self.testCasesPassed, self.testCasesRun, self.testClassesRun))
        if self.testCasesSkipped:
            _logger.info("  Skipped cases:")
            for tc in self.testCasesSkipped:
                _logger.info("    " + tc)
        if self.testCasesFailed:
            ok = False
            _logger.info("  Failed cases:")
            for tc in self.testCasesFailed:
                _logger.info("    " + tc)
        return ok
