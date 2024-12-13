from pyPhases.test.Mocks import OverwriteConfig
from pyPhases.test.TestCase import TestCase


class TestBaseTest(TestCase):
    phase = TestCase.project.phases[0]

    def tearDown(self):
        super().tearDown()
        self.assertNotIn("option1", self.project.config)
        self.assertNotIn("option2", self.project.config)

    def testConfigBefore(self):
        self.assertEqual(self.project.getConfig("option2", 6), 6)

    @OverwriteConfig({"option1": 1, "option2": 2})
    def testConfigMockDict(self):
        self.assertEqual(self.getConfig("option1"), 1)
        self.assertEqual(self.getConfig("option2"), 2)

    @OverwriteConfig(option1=3, option2=4)
    def testConfigMockArgs(self):
        self.assertEqual(self.getConfig("option1"), 3)
        self.assertEqual(self.getConfig("option2"), 4)

    def testConfigAfter(self):
        self.assertEqual(self.project.getConfig("option1", 5), 5)
