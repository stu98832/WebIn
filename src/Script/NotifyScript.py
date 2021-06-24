from datetime import datetime
import time 
from typing import Callable, List
from Core.Script.ScriptContext import ScriptContext
from Script.NotifyRecord import NotifyRecord
from Script.ScheduleTime import ScheduleTime
from Script.NotifyRecord import NotifyRecord
from Script.Http import Http
import bs4
import requests
from threading import Lock, Thread

class NotifyScript:
    Records: List[NotifyRecord]
    Context: ScriptContext
    NotifyEnter: Callable[['NotifyScript', NotifyRecord], None]

    def __init__(self, name: str):
        self.NotifyEnter = None
        self.Records = []
        self.Name = name
        self.Context = None
        self.Schedule = ScheduleTime.Parse('0 * * * *')
        self.Enable = True
        self.mScriptLock = Lock()
        self.mLogin = False
        self.mAliveTime = datetime.now()

    @staticmethod
    def FromDB(data, records):
        script = NotifyScript(data['name'])
        if data['script']:
            script.Context = ScriptContext(data['script'])
        script.Records = records
        script.Schedule = ScheduleTime.Parse(data['schedule'])
        script.Enable = data['enable'] == 1
        return script
    
    def Setup(self):
        if not self.Context:
            return
        self.Context.SetGlobalVariable('http', Http())
        self.Context.SetGlobalVariable('bs4', bs4)
        self.Context.SetGlobalVariable('requests', requests)
        setup = self.Context.GetGlobalVariable('setup')
        if setup:
            setup()
    
    def Alive(self):
        if not self.Context:
            return
        elapsed = (datetime.now() - self.mAliveTime)
        if elapsed.total_seconds() < 600:
            return
        self.mScriptLock.acquire()
        try:
            funcAlive = self.Context.GetGlobalVariable('alive')
            if self.mLogin and funcAlive:
                self.mLogin = funcAlive()
                self.mAliveTime = datetime.now()

                if not self.mLogin:
                    print('failed to alive')
                    # TODO: log failed
                    return
        except Exception as ex:
            print('alive-error', ex)
            # TODO: log except
        finally:
            self.mScriptLock.release()

    def Execute(self):
        if not self.Context:
            return
        self.mScriptLock.acquire()
        try:
            funcLogin = self.Context.GetGlobalVariable('login')

            if not self.mLogin and funcLogin:
                self.mLogin = funcLogin()
                self.mAliveTime = datetime.now()

                if not self.mLogin:
                    print('failed to login')
                    # TODO: log failed
                    return

            infos = self.Context.Call('listing')
            pending = []
            for info in infos:
                def fetchStage(info):
                    try:
                        data = self.Context.Call('fetch', info['data'])

                        # skip failed fetchs
                        if not data:
                            return

                        if not 'title' in data or not 'description' in data or not 'update_time' in data:
                            print('no data?')
                            # TODO: log script fetch error
                            return

                        # second skip for duplicate news
                        if (not info['key'] 
                            and (data['title'], data['description'], data['update_time']) 
                                in map(lambda x: (x.Title, x.Description, x.UpdateTime), self.Records)):
                            print('skip2', info)
                            return
                        
                        if not type(data['update_time']) is datetime:
                            raise TypeError('type of update_time should be datetime')

                        record = NotifyRecord()
                        record.Title = str(data['title'])
                        record.Description = str(data['description'])
                        record.Content = '' if not 'content' in data else str(data['content'])
                        record.UpdateTime = data['update_time']
                        record.IsRead = False
                        record.Key = str(info['key'])

                        self.Records.append(record)
                        if self.NotifyEnter:
                            self.NotifyEnter(self, record)
                    except Exception as ex:
                        print('fetch-error', ex)
                        # TODO: log except

                if not 'data' in info:
                    info['data'] = { }
                if not 'key' in info:
                    info['key'] = ''
                info['key'] = str(info['key'])

                # first skip for duplicate news
                if info['key'] in map(lambda x: x.Key, self.Records):
                    continue

                pending.append(Thread(target = fetchStage, args=(info,), daemon=True))

            while len(pending) > 0:
                threads = pending[:10]
                pending = pending[10:]
                for thread in threads:
                    thread: Thread
                    thread.start()
                    time.sleep(0.05)

                for thread in threads:
                    thread.join()
        except Exception as ex:
            print('execute-error', ex)
            # TODO: log except
        finally:
            self.mScriptLock.release()
