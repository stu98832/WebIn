from unittest import TestCase
from Script.ScheduleTime import ScheduleTime
from datetime import datetime

class TestScheduleTime(TestCase):
    
    def test_Parse(self):
        text = '10 * * * *'
        sche = ScheduleTime.Parse(text)
        self.assertEqual(str(sche), text)

    def test_15secPerMinute(self):
        sche = ScheduleTime(15)
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 0, 15)))
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 0, 0, 14)))

    def test_15sec30secPerMinute(self):
        sche = ScheduleTime([15, 30])
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 0, 15)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 0, 30)))
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 0, 0, 14)))
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 0, 0, 29)))

    def test_EveryTime(self):
        sche = ScheduleTime()
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 0, 0)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 0, 14)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 0, 15)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 0, 29)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 0, 30)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 0, 59)))

    def test_EverysecIn15minPerHour(self):
        sche = ScheduleTime(minu=15)
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 15, 0)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 15, 14)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 15, 15)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 15, 29)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 15, 30)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 0, 15, 59)))
        
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 0, 14, 0)))
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 0, 14, 14)))
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 0, 14, 15)))
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 0, 14, 29)))
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 0, 14, 30)))
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 0, 14, 59)))

    def test_Every20secPerMinuteIn15hour(self):
        sche = ScheduleTime(sec=[0, 20,40], hour=15)
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 15, 0, 0)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 15, 0, 20)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 15, 0, 40)))
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 15, 0, 10)))
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 15, 0, 30)))
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 15, 0, 50)))
        
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 15, 20, 0)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 15, 20, 20)))
        self.assertTrue(sche.CheckTime(datetime(2020, 10, 10, 15, 20, 40)))
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 15, 20, 10)))
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 15, 20, 30)))
        self.assertFalse(sche.CheckTime(datetime(2020, 10, 10, 15, 20, 50)))