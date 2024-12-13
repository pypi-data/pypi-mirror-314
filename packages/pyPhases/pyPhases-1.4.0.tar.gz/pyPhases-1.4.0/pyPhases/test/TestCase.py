import unittest
from typing import TypeVar, Type

from pyPhases.Phase import Phase
from pyPhases.Project import Project
from pyPhases.util.Logger import classLogger
from pyPhases.util.pdict import pdict

T = TypeVar('T')

class ProjectNotSetExeption(Exception):
    pass


@classLogger
class TestCase(unittest.TestCase):
    project: Project = None
    phase: Phase = None
    tmpConfig: dict = {}

    def __init__(self, methodName="runTest"):
        if TestCase.project is None:
            self.logError(
                "There is no Project set in static attribute TestCase.project, please use `phases test ...` to run your tests"
            )
        else:
            self.phase.project = TestCase.project
        super().__init__(methodName)
        self.restoreConfig = None
        self.cleanData = True

    def config(self):
        return None

    def data(self):
        return {}

    def getConfig(self, name):
        if name in self.tmpConfig:
            return self.tmpConfig[name]
        return self.phase.project.getConfig(name)

    def setConfig(self, name, value):
        self.tmpConfig[name] = value

    def getData(self, data, expectedReturnType: Type[T] = None) -> T:
        return self.phase.project.getData(data)

    def assertDataEqual(self, dataname, value):
        data = self.getData(dataname)
        self.assertEqual(data, value)

    def prepare(self) -> None:
        self.beforePrepare()
        if self.cleanData:
            TestCase.project.registeredData = {}
        config = self.config()
        config = pdict() if config is None else config
        registerData = self.data()
        self.phaseConfig = config

        TestCase.project.addConfig(config)
        TestCase.project.trigger("configChanged", None)

        for field, data in registerData.items():
            TestCase.project.registerData(field, data)

        if self.phase is not None:
            self.phase.prepare()

    def tearDown(self) -> None:
        TestCase.project.config = self.restoreConfig

    def setUp(self) -> None:
        self.restoreConfig = pdict(TestCase.project.config.copy())
        self.prepare()

    def beforePrepare(self):
        pass
