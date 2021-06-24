from unittest import TestCase
import time
from datetime import datetime
from Script.ScriptScheduler import ScriptScheduler
from Script.ScheduleTime import ScheduleTime

class MockScript:
    def __init__(self, name):
        self.Name = name
        self.ResultCount = 0
    
    def Setup(self):
        pass
    
    def Execute(self):
        self.ResultCount += 1

class MockDelayScript:
    def __init__(self, name):
        self.Name = name
        self.ResultCount = 0
    
    def Setup(self):
        pass
    
    def Execute(self):
        self.ResultCount += 1
        time.sleep(2.0)

class TestScriptScheduler(TestCase):
    def setUp(self):
        self.scheduler = ScriptScheduler()

    def tearDown(self):
        self.scheduler.mActive = False
    
    def test_GetSetScript(self):
        script123 = MockScript('123')
        self.scheduler.AddScript(script123, ScheduleTime())
        self.assertEqual(script123, self.scheduler.GetScript('123'))
    
    def test_SmallScheduleTest(self):
        script123 = MockScript('123')
        script456 = MockScript('456')
        self.scheduler.AddScript(script123, ScheduleTime([i for i in range(0, 60, 2)]))
        self.scheduler.AddScript(script456, ScheduleTime([i for i in range(0, 60, 4)]))
        time.sleep(4)
        self.assertEqual(script123.ResultCount, 2)
        self.assertEqual(script456.ResultCount, 1)
    
    def test_SmallScheduleDelayTest(self):
        script123 = MockDelayScript('123')
        script456 = MockDelayScript('456')
        self.scheduler.AddScript(script123, ScheduleTime([i for i in range(0, 60, 2)]))
        self.scheduler.AddScript(script456, ScheduleTime([i for i in range(0, 60, 4)]))
        time.sleep(4)
        self.assertEqual(script123.ResultCount, 2)
        self.assertEqual(script456.ResultCount, 1)
