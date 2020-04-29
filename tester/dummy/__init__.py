from overrides import overrides
from ..test import HarnessTest

# this demonstrates the overrides required for product-specific tests
# in this case we just NOP them all, except for providing an example override point for setup
# check out SandboxTest in the graviti repo for a more thorough example.
class DummyTest(HarnessTest):

    def dummySetup(self):
        pass

    @overrides
    def testSetUp(self):
        self.dummySetup()

    @overrides
    def testTearDown(self):
        pass

    @overrides
    def checkForReportedErrors(self):
        pass

    @overrides
    def logTestRemnants(self):
        pass

    @overrides
    def testLeaveRunningStatus(self):
        return None
