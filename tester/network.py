
import os
import logging
import json
import subprocess
import tempfile
import shutil

from .port_manager import portManager
from .ext import util


_logger = logging.getLogger(__name__)


class Network(object):

    def __init__(self, config = None, dockerImage = None, portManager = None):
        self.config = config or NetConfig()
        self.networkId = util.generateIdentifier(4)
        self._dockerImage = dockerImage
        self._basePath = os.path.join(tempfile.gettempdir(), "sandbox_{}".format(self.networkId))
        os.makedirs(self._basePath)
        self.manager = None
        self.agentJobs = []
        self.agents = []
        self.managerConfigPath = os.path.join(self._basePath, "sandbox.cfg")
        util.writeDataToFileAtPath(self.config.managerConfigJson(), self.managerConfigPath)
        self.portManager = portManager or portManager()
        if self._dockerImage:
            self.dockerNetwork = "sandbox_net_{}".format(self.networkId)
            # just create a local bridge network for now...
            subprocess.Popen(["docker", "network", "create", self.dockerNetwork], stdout=subprocess.DEVNULL)

    def addManager(self, start = True, port = None):
        NYI

    def addAgent(self, start = True):
        NYI

    def runningProcesses(self):
        return [self.manager] + self.agents

    def waitForStartup(self):
        NYI # tai
        #for rp in self.runningProcesses():
        #    rp.waitForStartup()

    def shutdown(self, cleanup = True):
        if True:
            _logger.warn("Shutdown NYI")
            return
        #for rp in self.runningProcesses():
        #    rp.shutdow(cleanup)
        if cleanup:
            shutil.rmtree(self._basePath)
            self._basePath = None
            if self._dockerImage:
                subprocess.Popen(["docker", "network", "rm", self.dockerNetwork], stdout=subprocess.DEVNULL)

    def logRemnants(self):
        _logger.warn("Network {} was using folder at:  {}".format(self.networkId, self._basePath))
        if self._dockerImage:
            _logger.warn("Network {} was using docker network:  {}".format(self.networkId, self.dockerNetwork))
        _logger.warn("logRemnants NYI")
        #for rp in self.runningProcesses():
        #    rp.logRemnants()

    def checkForReportedErrors(self):
        #for rp in self.runningProcesses():
        #    if rp.hasPanic():
        #        raise Exception("PANIC failure")
        _logger.warn("checkForReportedErrors NYI")



class NetConfig(object):

    def __init__(self, requireAgentAuthentication = True):
        self.requireAgentAuthentication = requireAgentAuthentication

    def managerConfigJson(self):
        return json.dumps({ "db" : { "host" : "127.0.0.1",
                                     "port" : 3306,
                                     "user" : "root",
                                     "password" : "",
                                     "db" : "sandbox" },
                            "agentBinaryPath" : "~/tmp/sandbox/agent",
                            "requireAgentAuthentication" : self.requireAgentAuthentication,
                            "contentStore" : {
                                "host" : "47.103.90.26",
                                "port" : "9101"
                            }})
