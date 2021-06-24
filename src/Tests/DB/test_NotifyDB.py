from unittest import TestCase
from DB.NotifyDB import NotifyDB
from Script.NotifyRecord import NotifyRecord
from Script.NotifyScript import NotifyScript
from Script.ScheduleTime import ScheduleTime
from datetime import datetime

class TestNotifyDB(TestCase):
    def setUp(self) -> None:
        self.db = NotifyDB(':memory:')
        self.db.mCursor.execute(
            "CREATE TABLE scripts (" + 
            "  name TEXT PRIMARY KEY," + 
            "  script TEXT DEFAULT ''," + 
            "  schedule TEXT DEFAULT '* * * * *'," + 
            "  enable INTEGER DEFAULT 1" + 
            ")" 
        )
        self.db.mCursor.execute(
            "CREATE TABLE `script_records` (" + 
            "  id INTEGER PRIMARY KEY AUTOINCREMENT," + 
            "  script_name TEXT," + 
            "  title TEXT DEFAULT ''," + 
            "  desc TEXT DEFAULT ''," + 
            "  content TEXT DEFAULT ''," + 
            "  update_time DATE DEFAULT '1970-01-01 00:00:00'," + 
            "  is_read INTEGER DEFAULT 0," + 
            "  key TEXT DEFAULT ''," + 
            "  FOREIGNER KEY script_name REFERENCES scripts(name)" + 
            ");" 
        )

    def tearDown(self) -> None:
        self.db.mConn.close()

    def test_InsertScript_GetScript(self):
        script = NotifyScript('test')
        script.Schedule = ScheduleTime.Parse('10 * * * *')
        try:
            self.db.InsertScript(script, commit=False)
            scriptDB = self.db.GetScript('test')
            self.assertEqual(script.Name, scriptDB.Name)
            self.assertIsNone(scriptDB.Context)
            self.assertEqual(len(script.Records), 0)
            self.assertEqual(str(script.Schedule), str(scriptDB.Schedule))
            self.assertEqual(script.Enable, scriptDB.Enable)
        except Exception as ex:
            raise ex
        finally:
            self.db.mConn.rollback()

    def test_UpdateScript_GetScript(self):
        script = NotifyScript('test')
        script.Schedule = ScheduleTime.Parse('10 * * * *')
        try:
            self.db.InsertScript(script, commit=False)
            scriptDB = self.db.GetScript('test')
            self.assertEqual(script.Name, scriptDB.Name)
            self.assertIsNone(scriptDB.Context)
            self.assertEqual(len(script.Records), 0)
            self.assertEqual(str(script.Schedule), str(scriptDB.Schedule))
            self.assertEqual(script.Enable, scriptDB.Enable)
            script.Name = 'test2'
            script.Enable = True
            script.Schedule = ScheduleTime.Parse('10,20 30 * * *')
            self.db.UpdateScript('test', script, commit=False)
            scriptDBOld = self.db.GetScript('test')
            scriptDB = self.db.GetScript('test2')
            self.assertIsNone(scriptDBOld)
            self.assertEqual(script.Name, scriptDB.Name)
            self.assertIsNone(scriptDB.Context)
            self.assertEqual(len(script.Records), 0)
            self.assertEqual(str(script.Schedule), str(scriptDB.Schedule))
            self.assertEqual(script.Enable, scriptDB.Enable)
        except Exception as ex:
            raise ex
        finally:
            self.db.mConn.rollback()

    def test_InsertScript_GetScript_withRecord(self):
        script = NotifyScript('test')
        script.Schedule = ScheduleTime.Parse('10 * * * *')
        for i in range(30):
            record = NotifyRecord()
            record.Title = 'record-{}'.format(i)
            record.Description = 'test-{}'.format(i)
            record.Content = 'hello-{}'.format(i)
            record.UpdateTime = datetime(2020, 10, i+1)
            record.IsRead = (i % 2) == 1
            record.Key = str(i)
            script.Records.append(record)
        try:
            self.db.InsertScript(script, commit=False)
            scriptDB = self.db.GetScript('test')
            self.assertEqual(script.Name, scriptDB.Name)
            self.assertIsNone(scriptDB.Context)
            self.assertEqual(str(script.Schedule), str(scriptDB.Schedule))
            self.assertEqual(len(script.Records), len(scriptDB.Records))
            for record in scriptDB.Records:
                record: NotifyRecord
                i = int(record.Title.split('-')[1])
                self.assertEqual(record.Title, 'record-{}'.format(i))
                self.assertEqual(record.Description, 'test-{}'.format(i))
                self.assertEqual(record.Content, 'hello-{}'.format(i))
                self.assertEqual(record.UpdateTime, datetime(2020, 10, i+1))
                self.assertEqual(record.IsRead, (i % 2) == 1)
                self.assertEqual(record.Key, str(i))
        except Exception as ex:
            raise ex
        finally:
            self.db.mConn.rollback()

    def test_UpdateRecord_GetScript(self):
        script = NotifyScript('test')
        script.Schedule = ScheduleTime.Parse('10 * * * *')
        record = NotifyRecord()
        record.Content = 'hello'
        record.IsRead = False
        record.Title = 'title'
        record.Description = 'description'
        record.UpdateTime = datetime(2020, 10, 20, 0, 0, 30)
        record.Key = '1'
        script.Records.append(record)
        try:
            self.db.InsertScript(script, commit=False)
            scriptDB = self.db.GetScript('test')
            self.assertEqual(script.Name, scriptDB.Name)
            self.assertIsNone(scriptDB.Context)
            self.assertEqual(len(script.Records), 1)
            self.assertEqual(str(script.Schedule), str(scriptDB.Schedule))
            self.assertEqual(script.Enable, scriptDB.Enable)
            self.assertEqual(scriptDB.Records[0].Title, 'title')
            self.assertEqual(scriptDB.Records[0].Description, 'description')
            self.assertEqual(scriptDB.Records[0].Content, 'hello')
            self.assertEqual(scriptDB.Records[0].UpdateTime, datetime(2020, 10, 20, 0, 0, 30))
            self.assertEqual(scriptDB.Records[0].IsRead, False)
            self.assertEqual(scriptDB.Records[0].Key, '1')
            scriptDB.Records[0].IsRead = True
            self.db.UpdateRecord(scriptDB.Records[0])
            recordsDB = self.db.GetRecords('test')
            self.assertEqual(len(recordsDB), 1)
            self.assertEqual(recordsDB[0].Title, 'title')
            self.assertEqual(recordsDB[0].Description, 'description')
            self.assertEqual(recordsDB[0].Content, 'hello')
            self.assertEqual(recordsDB[0].UpdateTime, datetime(2020, 10, 20, 0, 0, 30))
            self.assertEqual(recordsDB[0].IsRead, True)
            self.assertEqual(recordsDB[0].Key, '1')
        except Exception as ex:
            raise ex
        finally:
            self.db.mConn.rollback()
