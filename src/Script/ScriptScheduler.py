from threading import Thread
from datetime import datetime
import time
from typing import Dict, Tuple
from Script.NotifyScript import NotifyScript
from Script.ScheduleTime import ScheduleTime

class ScriptScheduler:
    def __init__(self):
        self.mScripts = { }
        self.mActive = False
        self.mScheduleThread = Thread(target=self._Schedule, daemon=True)
        self.Start()
    
    def Start(self):
        self.mActive = True
        self.mScheduleThread.start()

    def AddScript(self, script: NotifyScript, schedule: ScheduleTime):
        if script.Name not in self.mScripts:
            self.mScripts[script.Name] = (script, schedule)
            script.Setup()
        else:
            # TODO: Log duplicate script name
            pass

    def GetScript(self, name):
        if not name in self.mScripts:
            # TODO: Throw an error?
            return None
        return self.mScripts[name][0]

    def RemoveScript(self, name):
        if not name in self.mScripts:
            # TODO: Throw an error?
            return
        del self.mScripts[name]
    
    def _Schedule(self):
        # update every 0.3 seconds, 
        prev = datetime.now().replace(microsecond=0)
        while self.mActive:
            time.sleep(0.3)
            now = datetime.now().replace(microsecond=0)
            if prev == now:
                continue

            # update time and check script triggle time
            for name, (script, schedule) in self.mScripts.items():
                script: NotifyScript
                schedule: ScheduleTime

                script.Alive()
                # TODO: test CheckTime on heavy loading
                if schedule.CheckTime(now):
                    t = Thread(target=script.Execute, daemon=True)
                    t.start()
                    
            prev = now