import sqlite3
import os.path
from typing import List
from Script.NotifyRecord import NotifyRecord
from Script.NotifyScript import NotifyScript
from threading import Lock

class NotifyDB:
    def __init__(self, dbfile):
        exists = False
        if dbfile != ':memory:':
            exists = os.path.exists(dbfile)
        self.mConn = sqlite3.connect(dbfile, check_same_thread=False)
        self.mConn.row_factory = sqlite3.Row
        self.mCursor = self.mConn.cursor()
        self.mLock = Lock()
        if not exists:
            self._CreateTables()
    
    @staticmethod
    def BuildIn():
        db = NotifyDB(':memory:')
        return db

    def _CreateTables(self):
        self.mCursor.execute(
            "CREATE TABLE scripts (" + 
            "  name TEXT PRIMARY KEY," + 
            "  script TEXT DEFAULT ''," + 
            "  schedule TEXT DEFAULT '* * * * *'," + 
            "  enable INTEGER DEFAULT 1" + 
            ")" 
        )
        self.mCursor.execute(
            "CREATE TABLE `script_records` (" + 
            "  script_name TEXT," + 
            "  title TEXT DEFAULT ''," + 
            "  desc TEXT DEFAULT ''," + 
            "  content TEXT DEFAULT ''," + 
            "  update_time DATE DEFAULT '1970-01-01 00:00:00'," + 
            "  is_read INTEGER DEFAULT 0," + 
            "  key TEXT DEFAULT ''," + 
            "  FOREIGNER KEY script_name REFERENCES scripts(name)" + 
            ")" 
        )
        self.mConn.commit()
    
    def Rollback(self):
        self.mConn.rollback()
    
    def Commit(self):
        self.mConn.commit()

    def InsertScript(self, script: NotifyScript, commit=True):
        self.mLock.acquire()
        try:
            sql = "INSERT INTO scripts (`name`,`script`,`schedule`,`enable`) VALUES (?,?,?,?);"
            self.mCursor.execute(sql, (script.Name, script.Context.Name if script.Context else '', str(script.Schedule), script.Enable))
            sql = (
                "INSERT INTO script_records (`script_name`,`title`,`desc`,`content`,`update_time`,`is_read`, `key`)" + 
                " VALUES (?,?,?,?,?,?,?);"
            )
            for record in script.Records:
                self.mCursor.execute(sql, (
                    script.Name, 
                    record.Title,
                    record.Description,
                    record.Content,
                    record.UpdateTime.strftime('%Y:%m:%d %H:%M:%S'), 
                    1 if record.IsRead else 0,
                    record.Key
                ))
            if commit:
                self.mConn.commit()
        except Exception as ex:
            if commit:
                self.mConn.rollback()
            raise sqlite3.DatabaseError('DBError: failed insert script. SQL="{}"'.format(sql), ex)
        finally:
            self.mLock.release()
    
    def DeleteScript(self, script: NotifyScript, commit = True):
        self.mLock.acquire()
        try:
            sql = 'DELETE FROM script_records WHERE `script_name`=?'
            self.mCursor.execute(sql, (script.Name,))
            sql = 'DELETE FROM scripts WHERE `name`=?'
            self.mCursor.execute(sql, (script.Name,))
            if commit:
                self.mConn.commit()
        except Exception as ex:
            if commit:
                self.mConn.rollback()
            raise sqlite3.DatabaseError('DBError: failed delete script. SQL="{}"'.format(sql), ex)
        finally:
            self.mLock.release()

    def UpdateScript(self, oldname, script: NotifyScript, commit=True):
        self.mLock.acquire()
        try:
            sql = "UPDATE scripts SET `name`=?,`script`=?,`schedule`=?,`enable`=? WHERE `name`=?;"
            self.mCursor.execute(sql, (script.Name, script.Context.Name if script.Context else '', str(script.Schedule), script.Enable, oldname))
            sql = "UPDATE script_records SET `script_name`=? WHERE `script_name`=?;"
            self.mCursor.execute(sql, (script.Name, oldname))
            if commit:
                self.mConn.commit()
        except Exception as ex:
            if commit:
                self.mConn.rollback()
            raise sqlite3.DatabaseError('DBError: failed insert script. SQL="{}"'.format(sql), ex)
        finally:
            self.mLock.release()

    def UpdateRecords(self, records: List[NotifyRecord], commit=True):
        self.mLock.acquire()
        try:
            sql = "UPDATE script_records SET `title`=?,`desc`=?,`content`=?,`update_time`=?,`is_read`=?, `key`=? WHERE `rowid`=?;"
            self.mCursor.executemany(sql, [(
                record.Title,
                record.Description,
                record.Content,
                record.UpdateTime.strftime('%Y:%m:%d %H:%M:%S'), 
                1 if record.IsRead else 0,
                record.Key,
                record.ID
            ) for record in filter(lambda x: x.ID != -1, records)])
            if commit:
                self.mConn.commit()
        except Exception as ex:
            if commit:
                self.mConn.rollback()
            raise sqlite3.DatabaseError('DBError: failed update record. SQL="{}"'.format(sql), ex)
        finally:
            self.mLock.release()

    def UpdateRecord(self, record: NotifyRecord, commit=True):
        self.mLock.acquire()
        try:
            sql = "UPDATE script_records SET `title`=?,`desc`=?,`content`=?,`update_time`=?,`is_read`=?, `key`=? WHERE `rowid`=?;"
            self.mCursor.execute(sql, (
                record.Title,
                record.Description,
                record.Content,
                record.UpdateTime.strftime('%Y:%m:%d %H:%M:%S'), 
                1 if record.IsRead else 0,
                record.Key,
                record.ID
            ))
            if commit:
                self.mConn.commit()
        except Exception as ex:
            if commit:
                self.mConn.rollback()
            raise sqlite3.DatabaseError('DBError: failed update record. SQL="{}"'.format(sql), ex)
        finally:
            self.mLock.release()
    
    def InsertRecord(self, script: NotifyScript, record: NotifyRecord, commit=True):
        self.mLock.acquire()
        try:
            sql = (
                "INSERT INTO script_records (`script_name`,`title`,`desc`,`content`,`update_time`,`is_read`, `key`)" + 
                " VALUES (?,?,?,?,?,?,?);"
            )
            self.mCursor.execute(sql, (
                script.Name, 
                record.Title,
                record.Description,
                record.Content,
                record.UpdateTime.strftime('%Y:%m:%d %H:%M:%S'), 
                1 if record.IsRead else 0,
                record.Key
            ))
            sql = "SELECT rowid FROM script_records ORDER BY rowid DESC LIMIT 1"
            self.mCursor.execute(sql)
            record.ID = self.mCursor.fetchone()['rowid']
            if commit:
                self.mConn.commit()
        except Exception as ex:
            if commit:
                self.mConn.rollback()
            print(ex)
            raise sqlite3.DatabaseError('DBError: failed insert record. SQL="{}"'.format(sql), ex)
        finally:
            self.mLock.release()

    def GetRecords(self, script_name: str):
        records = []
        try:
            sql = "SELECT rowid as id, * FROM script_records WHERE `script_name`=?"
            self.mCursor.execute(sql, (script_name,))

            for row in self.mCursor.fetchall():
                records.append(NotifyRecord.FromDB(row))
        except Exception as ex:
            print(ex)
        return records
    
    def GetScript(self, name: str):
        self.mLock.acquire()
        try:
            sql = "SELECT * FROM scripts WHERE `name`=?"
            self.mCursor.execute(sql, (name,))
    
            data = self.mCursor.fetchone()
        finally:
            self.mLock.release()
        if data:
            script = NotifyScript.FromDB(data, self.GetRecords(data['name']))
            return script
        return None

    def GetScripts(self):
        scripts = []
        sql = "SELECT * FROM scripts"
        self.mCursor.execute(sql)

        scripts: List[NotifyScript]
        for row in self.mCursor.fetchall():
            notify = self.GetScript(row['name'])
            if notify:
                scripts.append(notify)
        return scripts
