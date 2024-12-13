import importlib
import json
from pathlib import Path
from unittest import TestCase
from pyPhases.Data import Data, DataNotFound
from pyPhases.Project import ConfigNotFoundException, Project, PhaseNotFoundException
from pyPhases.decorator.Decorator import Decorator
from pyPhases.exporter.PickleExporter import PickleExporter
from unittest.mock import MagicMock, call, patch, mock_open
from pyPhases.Phase import Phase
from pyPhases.util.pdict import pdict
from pyPhases.exporter import DataExporter

class MockExporter(DataExporter):
    pass

class AnotherMockExporter(DataExporter):
    pass

class OneMoreMockExporter(DataExporter):
    pass

class TestProject(TestCase):
    def test_registerDecorator(self):
        decorator = Decorator()
        project = Project()
        project.registerDecorator(decorator)
        self.assertIn(decorator, project.decorators)

    def test_registerExporter(self):
        exporter = PickleExporter()
        project = Project()
        project.registerExporter(exporter)
        self.assertIn(exporter, project.exporters)

    def test_register_exporter_priority(self):
        # Test registering a basic exporter
        exporter = MockExporter()
        project = Project()

        project.registerExporter(exporter)
        self.assertEqual(len(project.exporters), 1)
        self.assertEqual(project.exporters[0], exporter)

        # Test default priority
        self.assertEqual(exporter.priority, 100)

        # Test registering exporter with custom priority
        exporter2 = MagicMock()
        project.registerExporter(exporter2, priority=50)
        self.assertEqual(len(project.exporters), 2)
        self.assertEqual(project.exporters[1], exporter2)
        self.assertEqual(exporter2.priority, 50)

        # Test exporters sorted by priority
        exporter3 = MagicMock()
        project.registerExporter(exporter3, priority=150)
        self.assertEqual(len(project.exporters), 3)
        self.assertEqual(project.exporters[0], exporter3)
        self.assertEqual(project.exporters[1], exporter)
        self.assertEqual(project.exporters[2], exporter2)


    def test_getExporterForIntsance(self):
        project = Project()
        project.getExporterForType = MagicMock()

        project.getExporterForIntsance("test")
        project.getExporterForType.assert_called_with(str)

        project.getExporterForIntsance(5)
        project.getExporterForType.assert_called_with(int)

        class A:
            pass

        project.getExporterForIntsance(A())
        project.getExporterForType.assert_called_with(A)

    def test_getExporterForType(self):
        project = Project()

        self.assertEqual(project.getExporterForType(None), None)
        self.assertEqual(project.getExporterForType(str), None)

        exporter = PickleExporter()
        project.registerExporter(exporter)
        self.assertEqual(project.getExporterForType(str, reinit=False), exporter)

        self.assertNotEqual(project.getExporterForType(str, reinit=True), exporter)
        self.assertIsInstance(project.getExporterForType(str, reinit=True), PickleExporter)

    def test_getDataFromName(self):
        project = Project()
        Data("test", project)
        dataObj = project.getDataFromName("test", "testversion")

        self.assertEqual(dataObj.name, "test")
        self.assertEqual(dataObj.version, "testversion")
        self.assertEqual(dataObj.project, project)

    def test_registerStreamExporterNotExist(self):
        project = Project()
        Data("test", project)

        self.assertRaises(Exception, project.registerStream, "test", str, {})

    def test_registerStream(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)

        project.registerStream("test", str, {"foo": "bar"})

        exporter.reinit.assert_called_once()
        exporterObject.stream.assert_called_with("test--current", {"foo": "bar"})

    def test_getExporterAndId(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporter, id = project.getExporterAndId("test", str)
        self.assertIsInstance(exporter, PickleExporter)
        self.assertEqual(id, "test--current")

    def test_getExporterAndIdNoExporter(self):
        project = Project()
        Data("test", project)
        exporter, id = project.getExporterAndId("test", str)
        self.assertEqual(exporter, None)
        self.assertEqual(id, "test--current")

    def test_getExporterAndIdNoData(self):
        project = Project()
        self.assertRaises(Exception, project.getExporterAndId, "test", str)

    def test_dataExists(self):
        project = Project()
        dataObj = Data("test", project)

        project.registerData("test", "myTestStr")

        self.assertTrue(project.dataExists(dataObj))
        self.assertFalse(project.dataExists(Data("test2", project)))

    def test_dataExistIn(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)

        project.dataExistIn("test", str, "testversion")

        exporter.reinit.assert_called_once()
        exporterObject.exists.assert_called_with("test--testversion")

    def test_dataExistInIsRegistered(self):
        project = Project()
        Data("test", project)

        project.registerData("test", "test")

        exist = project.dataExistIn("test", str)
        self.assertTrue(exist)

    def test_dataExistInNoExporter(self):
        project = Project()
        Data("test", project)

        r = project.dataExistIn("test", str, "testversion")

        self.assertEqual(r, False)

    def test_unregister(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)

        project.registeredData["test--testversion"] = "test"

        project.unregister("test", str, "testversion", options={"foo": "bar"})

        self.assertNotIn("test--testversion", project.registeredData)

    def test_unregisterNonExisting(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)

        self.assertRaises(
            KeyError,
            project.unregister,
            "test",
            str,
            "testversion",
            options={"foo": "bar"},
        )

    def test_getDataRegistered(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)

        project.registeredData["test--testversion"] = "test"

        data = project.getData("test", str, "testversion", options={"foo": "bar"})

        self.assertEqual(data, "test")

    def test_getDataExporter(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)

        project.getData("test", str, "testversion", options={"foo": "bar"})

        exporterObject.read.assert_called_with("test--testversion", {"foo": "bar"})

    def test_getDataGenerate(self):
        project = Project()
        project.generateData = MagicMock()
        Data("test", project)

        project.getData("test", str, "current", options={"foo": "bar"})
        project.generateData.called_once_with("test", str, "current", options={"foo": "bar"})

    def test_generateData(self):
        project = Project()
        phase = Phase([Data("dataname", project)])
        project.addPhaseAndPrepare(phase)

        def generateData(id):
            phase.registerData("dataname", "test")

        phase.generateData = generateData

        teststr = project.generateData("dataname", str, "current")
        self.assertEqual(teststr, "test")
        self.assertEqual(project.registeredData["dataname--current"], "test")

    def test_generateDataWithoutRegister(self):
        project = Project()
        phase = Phase([Data("test", project)])
        project.addPhaseAndPrepare(phase)

        def generateData(id):
            return "test"

        phase.generateData = generateData

        teststr = project.generateData("test", str, "current")
        self.assertEqual(teststr, "test")
        self.assertNotIn("dataname--current", project.registeredData)

    def test_getDataGenerateNoGeneration(self):
        project = Project()
        phase = Phase([Data("test", project)])
        project.addPhaseAndPrepare(phase)

        self.assertRaises(
            DataNotFound,
            project.generateData,
            "test",
            str,
            "current",
            options={"foo": "bar"},
        )

    def test_registerData(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)
        exporter.dataHandler = False

        project.registerData("test", "teststr", version="testversion", options={"foo": "bar"})

        exporterObject.write.assert_called_with("test--testversion", "teststr", {"foo": "bar"})
        self.assertEqual(exporterObject.currentDataObj, project.dataNames["test"])
        self.assertEqual(project.registeredData["test--testversion"], "teststr")

    def test_registerDataNoSave(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.dataHandler = False
        exporter.reinit = MagicMock(return_value=exporterObject)

        project.registerData("test", "teststr", version="testversion", options={"foo": "bar"}, save=False)

        exporterObject.write.assert_not_called()
        self.assertEqual(project.registeredData["test--testversion"], "teststr")

    def test_setConfig(self):
        project = Project()
        project.setConfig("test", "test")
        self.assertEqual(project.config["test"], "test")

    def test_getConfig(self):
        project = Project()
        project.config["test"] = "test"
        self.assertEqual(project.getConfig("test"), "test")

    def test_getConfigDotNotation(self):
        project = Project()
        project.config["test"] = {"blub": "test"}
        self.assertEqual(project.getConfig("test.blub"), "test")

    def test_getConfigKeyError(self):
        project = Project()
        self.assertRaises(ConfigNotFoundException, project.getConfig, "test")

    def test_setConfigKeyError(self):
        project = Project()
        self.assertRaises(KeyError, project.setConfig, "test.blub", 5)

    def get_getConfigDefault(self):
        project = Project()
        self.assertEqual(project.getConfig("nonExisting", "def"), "def")

    def get_getConfigDefaultDot(self):
        project = Project()
        self.assertEqual(project.getConfig("nonExisting.test", "def"), "def")

    def get_getConfigNotOverwrite(self):
        project = Project()
        self.assertEqual(project.getConfig("nonExisting.test", "def"), "def")
        self.assertRaises(ConfigNotFoundException, project.getConfig, "nonExisting.test")

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_saveConfig(self, m):
        json.dump = MagicMock()
        project = Project()
        project.setConfig("foo", "bar")

        m.return_value.__enter__.return_value = "data"
        project.saveConfig("myConfig.json")

        m.assert_called_with("myConfig.json", "w+")
        json.dump.assert_called_with({"foo": "bar"}, "data")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_saveConfig_tailor(self, m):
        json.dump = MagicMock()
        project = Project()
        Data("test", project, ["subconfig"])
        project.config = {"subconfig": {"foo": "bar"}, "othervalue": "test"}
        m.return_value.__enter__.return_value = "data"

        project.saveConfig("myConfig.json", "test")

        m.assert_called_with("myConfig.json", "w+")
        json.dump.assert_called_with({"subconfig": {"foo": "bar"}}, "data")

    def test_importConfigsByImportValue(self):
        project = Project()
        project.loadConfig = MagicMock(return_value="a")
        filePath = "/test1/test2/test3/test.yaml"
        baseConfig = {
            "foo": "bar",
            "test": [
                "../test.yml",
                "b.yml",
            ],
        }
        r = project.importConfigsByImportValue("test", baseConfig, filePath)

        project.loadConfig.assert_has_calls(
            [
                call(Path("/test1/test2/test3/../test.yml")),
                call(Path("/test1/test2/test3/b.yml")),
            ]
        )

        self.assertEqual(r, ["a", "a"])
        self.assertEqual(baseConfig, {"foo": "bar"})

    @patch("builtins.open", new_callable=mock_open, read_data='{"foo": "bar"}')
    def test_loadConfig(self, m):
        project = Project()
        project.config = pdict()

        config = project.loadConfig("myConfig.json")

        m.assert_called_with("myConfig.json", "r")
        self.assertIn("foo", config)
        self.assertEqual(config["foo"], "bar")
        self.assertEqual(project.config, {})

    @patch("builtins.open", new_callable=mock_open, read_data='{"foo": "bar"}')
    def test_loadAndApplyConfig(self, m):
        project = Project()
        project.config = {"a": "b"}

        config = project.loadAndApplyConfig("myConfig.json")

        m.assert_called_with("myConfig.json", "r")
        self.assertEqual(config, {"foo": "bar"})
        self.assertEqual(project.config, {"a": "b", "foo": "bar"})

    def test_addConfig(self):
        project = Project()
        project.config = pdict({"foo": "keep", "foofoo": {"bar": "overwrite", "foo2": "keep"}})
        updateConfig = pdict({"foo2": "add", "foofoo": {"bar": "foo", "bar2": "add"}})
        project.addConfig(updateConfig)

        self.assertEqual(
            project.config,
            {
                "foo": "keep",
                "foo2": "add",
                "foofoo": {"bar": "foo", "foo2": "keep", "bar2": "add"},
            },
        )

    def test_addPhaseAndPrepare(self):
        project = Project()
        phase = Phase()
        project.addPhaseAndPrepare(phase)
        self.assertEqual(project.phases[0], phase)
        self.assertEqual(project.phases[0].name, "Phase")
        self.assertEqual(project.phaseMap["Phase"], phase)

    def test_addPhaseAndPrepareWithName(self):
        project = Project()
        phase = Phase()
        project.addPhaseAndPrepare(phase, "test")
        self.assertEqual(project.phases[0], phase)
        self.assertEqual(project.phases[0].name, "test")
        self.assertEqual(project.phaseMap["test"], phase)

    @patch("pathlib.Path.exists", return_value=True)
    def test_addPlugin(self, m):
        project = Project()

        project.loadConfig = MagicMock(return_value={"foo2": "bar2"})
        pluginModule = MagicMock()
        importlib.import_module = MagicMock(return_value=pluginModule)

        pluginModule.__file__ = "pluginPath"
        project.addPlugin("myPlugin", {"foo": "bar"})

        plugin = importlib.import_module.return_value.Plugin
        pluginObj = importlib.import_module.return_value.Plugin.return_value

        importlib.import_module.assert_called_once_with(".Plugin", package="myPlugin")
        plugin.assert_called_once_with(project, {"foo": "bar"})
        self.assertEqual(project.plugins[0], pluginObj)
        pluginObj.initPlugin.assert_not_called()
        project.trigger("configChanged", None)
        pluginObj.initPlugin.assert_called_once()

        self.assertEqual(project.config, {"foo2": "bar2"})

    def test_prepareAllPhases(self):
        project = Project()
        phase = MagicMock()
        project.addPhaseAndPrepare(phase)

        phase.prepare.assert_called_once()
        phase.prepare.reset_mock()

        project.prepareAllPhases()

        phase.prepare.assert_called_once()

    def test_run(self):
        project = Project()
        phase = Phase()
        phase.run = MagicMock()
        project.addPhaseAndPrepare(phase)

        project.run("Phase")

        phase.run.assert_called_once()

    def test_runPhase(self):
        project = Project()
        phase = Phase()
        project.addPhaseAndPrepare(phase)
        project.trigger = MagicMock()
        phase.run = MagicMock()

        project.runPhase(phase)

        phase.run.assert_called_once()
        project.trigger.called_once_with("afterRun")

    def test_getPhase(self):
        project = Project()
        phase = Phase()
        project.addPhaseAndPrepare(phase)

        self.assertEqual(project.getPhase("Phase"), phase)

    def test_getPhaseNotExist(self):
        project = Project()
        self.assertRaises(PhaseNotFoundException, project.getPhase, "Phase")

    def test_enterContext(self):
        project = Project()
        project.config = pdict({"foo": "bar"})
        project.trigger = MagicMock()

        with project as p:
            p.setConfig("foo", "bar2")
            self.assertEqual(project.config["foo"], "bar2")
            project.trigger.assert_called_once_with("configChanged", "foo")

        self.assertEqual(project.config["foo"], "bar")
        project.trigger.assert_called_with("configChanged", None)

    def test_nestedContexts(self):
        project = Project()
        project.config = pdict({"foo": "bar"})
        project.trigger = MagicMock()

        with project as p:
            p.setConfig("foo", "bar2")
            self.assertEqual(project.config["foo"], "bar2")
            project.trigger.assert_called_once_with("configChanged", "foo")

            with p:
                p.setConfig("foo", "bar3")
                self.assertEqual(project.config["foo"], "bar3")
                project.trigger.assert_called_with("configChanged", "foo")

            self.assertEqual(project.config["foo"], "bar2")

        self.assertEqual(project.config["foo"], "bar")
        project.trigger.assert_called_with("configChanged", None)
