import signal
import sys
from typing import List
from PySide2.QtWidgets import QAction, QApplication, QSystemTrayIcon, QMenu
from GUI import ScriptManage
# from GUI.SettingForm import SettingForm
from Notify.NotifyManager import NotifyManager
from Script.NotifyRecord import NotifyRecord
from Script.NotifyScript import NotifyScript
from Script.ScriptScheduler import ScriptScheduler
from DB.NotifyDB import NotifyDB
import Config
import Resource

class NotifyApp(QApplication):
    ''' Main App Class '''

    mActQuit: QAction
    mActOpenManager: QAction
    mActClearNotify: QAction

    def __init__(self):
        super().__init__()
        if not Config.LoadFromJson('setting.json'):
            Config.LoadDefault()
            Config.SaveToJson('setting.json')
        sys.path.append(Resource.GetExtensionPath())
        self.mScheduler = ScriptScheduler()
        self.mDB = NotifyDB('data.db')
        self.mNotifyMgr = NotifyManager(
            self, 
            int(Config.Get('notify')['max-count']),
            Config.Get('notify')['duration'] / 1000.0)
        self._InitializeCmponent()
        self._LoadScript()
    
    def Run(self):
        self.exec_()
    
    def Exit(self):
        Config.SaveToJson('setting.json')
        self.quit()

    def _InitializeCmponent(self):
        ''' 元件初始化 '''

        # 腳本管理界面
        self.mScriptManageForm = ScriptManage.Form()
        self.mScriptManageForm.ScriptModified = self._OnScriptModified
        self.mScriptManageForm.ScriptCreated  = self._OnScriptCreated
        self.mScriptManageForm.ScriptRemove   = self._OnScriptRemove
        self.mScriptManageForm.RecordRead     = self._OnRecordRead
        self.mScriptManageForm.RecordReadAll  = self._OnRecordReadAll
        self.mScriptManageForm.ManagerHidden  = self._OnManagerHidden

        # 初始化選單
        self.mMenu = QMenu()
        self.mMenu.triggered.connect(self._OnMenuTriggered)
        self.mActOpenManager = self.mMenu.addAction('腳本管理')
        self.mActClearNotify = self.mMenu.addAction('清除右側通知')
        self.mMenu.addSeparator()
        self.mActQuit = self.mMenu.addAction('關閉')

        # 加入事件
        self.mIconify = QSystemTrayIcon()
        self.mIconify.setIcon(Resource.GetIconNew('favicon'))
        self.mIconify.setContextMenu(self.mMenu)
        self.mIconify.show()

    def _LoadScript(self):
        scripts = self.mDB.GetScripts()
        self.mScriptManageForm.LoadScripts(scripts)
        for script in scripts:
            script.NotifyEnter = self._OnNotifyEnter
            if script.Context and script.Enable:
                self.mScheduler.AddScript(script, script.Schedule)
    
    def _OnManagerHidden(self):
        self.mIconify.showMessage('WenIN', '已縮小到訊息列\n可對圖示點擊右鍵開啟選單')
    
    def _OnScriptModified(self, script: NotifyScript, oldName: str):
        self.mDB.UpdateScript(oldName, script)

        # 更新腳本設定後，會重新啟用腳本
        self.mScheduler.RemoveScript(oldName)
        if script.Context and script.Enable:
            self.mScheduler.AddScript(script, script.Schedule)
    
    def _OnScriptRemove(self, script: NotifyScript):
        self.mDB.DeleteScript(script)

        # 刪除腳本設定後，會關閉腳本
        self.mScheduler.RemoveScript(script.Name)
    
    def _OnScriptCreated(self, script: NotifyScript):
        self.mDB.InsertScript(script)

        # 設定委派，並加入排程
        script.NotifyEnter = self._OnNotifyEnter
        if script.Context and script.Enable:
            self.mScheduler.AddScript(script, script.Schedule)
    
    def _OnRecordRead(self, script: NotifyScript, record: NotifyRecord):
        self.mDB.UpdateRecord(record)

    def _OnRecordReadAll(self, script: NotifyScript, records: List[NotifyRecord]):
        self.mDB.UpdateRecords(records)

    def _OnNotifyEnter(self, script: NotifyScript, record: NotifyRecord):
        self.mDB.InsertRecord(script, record)
        self.mNotifyMgr.PushNotify(record.Title, record.Description)

    def _OnMenuTriggered(self, action: QAction):
        ''' 處理點擊選單事件 '''

        if action == self.mActQuit:
            self.Exit()
        elif action == self.mActOpenManager:
            self.mScriptManageForm.show()
        elif action == self.mActClearNotify:
            self.mNotifyMgr.Clear()