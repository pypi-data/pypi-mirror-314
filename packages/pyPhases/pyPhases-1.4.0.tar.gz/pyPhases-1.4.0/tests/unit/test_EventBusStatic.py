import unittest
from pyPhases.util.EventBusStatic import EventBusStatic

class EventBusStaticTest(unittest.TestCase):
    def test_on(self):
        EventBusStatic.eventMap = {}
        event_name = "event1"
        function = lambda x: x + 1

        EventBusStatic.on(event_name, function)

        self.assertEqual(EventBusStatic.eventMap[event_name], [function])

    def test_once(self):
        EventBusStatic.eventMap = {}
        event_name = "event2"
        function = lambda x: x * 2

        # Add the function twice
        EventBusStatic.once(event_name, function)
        EventBusStatic.once(event_name, function)

        self.assertEqual(EventBusStatic.eventMap[event_name], [function])

    def test_trigger(self):
        EventBusStatic.eventMap = {}
        event_name = "event3"
        results = []

        def function1(x):
            results.append(x)

        def function2(x):
            results.append(x + 1)

        EventBusStatic.on(event_name, function1)
        EventBusStatic.on(event_name, function2)

        EventBusStatic.trigger(event_name, 3)

        self.assertEqual(results, [3, 4])
