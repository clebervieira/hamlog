import logging
from enum import Enum

from .ext import DynamicArray


_logger = logging.getLogger(__name__)


class PortManager(object):
    ''' NOT optimized nor thread safe! '''

    ## Some ports to avoid in case we're using them for other local testing.
    _s_reservedPorts = [
          22,  # SSH
          80,  # HTTP
         443,  # HTTPS
        3306,  # MySQL default
        3888,  # jjsa random default
        5000,  # Docker Registries
      #33060,  # MySQL Extended X Protocol default
    ]

    class _Status(Enum):
        UNUSED = 0
        RESERVED = 1
        USED = 2
        USED_AND_RESERVED = 3

    def __init__(self, minPort = None, maxPort = None, reservedList = None, skipSetup = False):
        self.isSetup = False
        if not skipSetup:
            self._setup(minPort, maxPort, reservedList)

    def _setup(self, minPort = None, maxPort = None, reservedList = None):
        assert(not self.isSetup)
        self.isSetup = True
        self._minPort = minPort or 1025
        self._maxPort = maxPort or 65534
        self._usedPorts = DynamicArray(PortManager._Status.UNUSED)
        for p in (reservedList or PortManager._s_reservedPorts):
            self._usedPorts[p] = PortManager._Status.RESERVED

    def returnPort(self, p):
        assert(self._usedPorts[p] in (PortManager._Status.USED, PortManager._Status.USED_AND_RESERVED))
        if self._usedPorts[p] == PortManager._Status.USED_AND_RESERVED:
            self._usedPorts[p] = PortManager._Status.RESERVED
        else:
            self._usedPorts[p] = PortManager._Status.UNUSED

    def getPort(self, preferred = None):
        if preferred:
            if self._usedPorts[preferred] == PortManager._Status.UNUSED:
                self._usedPorts[preferred] = PortManager._Status.USED
                return preferred
            elif self._usedPorts[preferred] == PortManager._Status.RESERVED:
                _logger.warn("using reserved port {} as requested.".format(preferred))
                self._usedPorts[preferred] = PortManager._Status.USED_AND_RESERVED
                return preferred
            _logger.warn("preferred port {} already allocated.  finding another...".format(preferred))
        for p in range(self._minPort, self._maxPort + 1):
            if self._usedPorts[p] == PortManager._Status.UNUSED:
                self._usedPorts[p] = PortManager._Status.USED
                return p
        raise Exception("Out of ports!")

globalPortManager = PortManager(skipSetup = True)

def portManager(minPort = None, maxPort = None, reservedList = None):
    if not globalPortManager.isSetup:
        globalPortManager._setup(minPort, maxPort, reservedList)
    return globalPortManager
