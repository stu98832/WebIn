import os.path
from typing import Callable, Dict, List
from Core.Script.ScriptContext import ScriptContext
from PySide2.QtGui import QCloseEvent, QDesktopServices, QIcon
from PySide2.QtWidgets import (
    QMessageBox as MB,
    QPushButton,
    QTableWidgetItem,
    QWidget,
)
from PySide2.QtCore import QSize, QTimer, Qt
from Script.NotifyRecord import NotifyRecord
from Script.NotifyScript import NotifyScript
from Script.ScheduleTime import ScheduleTime
from . import Design
import App
import Resource
import functools

class Form(Design.UI):
    UI_FILE = 'main'

    mApp: 'App.NotifyApp'
    ScriptModified: Callable[[NotifyScript, str], None]
    ScriptCreated: Callable[[NotifyScript], None]
    ScriptRemove: Callable[[NotifyScript], None]
    RecordRead: Callable[[NotifyScript, NotifyRecord], None]
    RecordReadAll: Callable[[NotifyScript, List[NotifyRecord]], None]
    ManagerHidden: Callable[[], None]

    MODE_NORMAL = 0
    MODE_EDITED = 1
    MODE_CREATE = 2

    def __init__(self) -> None:
        super().__init__()
        self.mScripts = { }
        self.mTempScript = None
        self.mCurrentScript = None
        self.ScriptRemove = None
        self.ScriptCreated = None
        self.ScriptModified = None
        self.RecordRead = None
        self.RecordReadAll = None
        self.mReloadListTimer = QTimer()
        self.mReloadListTimer.setInterval(5000)
        self.mReloadListTimer.timeout.connect(self.RefreshList)
        self.mReloadListTimer.start()
        self.ReloadScriptList(self.mScripts)
    
    def LoadScripts(self, scripts: List[NotifyScript]):
        self.mScripts = dict((x.Name, x) for x in scripts)
        self.RefreshList()
    
    def RefreshList(self):
        self.ReloadScriptList(self.mScripts)
    
    def ReloadScript(self):
        self.OnLoadScriptDetails(self.mCurrentScript)

    def CheckNewScriptSave(self):
        if self.mTempScript != None:
            if MB.Cancel == self.Msgbox('確認', '有未儲存的新腳本，要捨棄嗎？', MB.Yes | MB.Cancel, MB.Warning):
                return False
            self.mTempScript = None
        return True

    def OnLoadScriptDetails(self, script: NotifyScript):
        self.mCurrentScript = script
        self.mTabControl.removeTab(0)
        self.mTabControl.removeTab(0)
        self.mTabHistory.hide()
        self.mTabScriptSetting.hide()
        self.mBtnSaveScript.hide()
        self.mBtnDeleteScript.hide()
        self.mBtnReadAll.hide()
        self.mBtnReloadRecord.hide()
        self.mTextHistoryContent.hide()
        if not script:
            self.mContentHint.show()
            self.mTabControl.hide()
            self.mLabelTitle.setText('')
            self.mTextScriptName.setText('')
        else:
            self.mContentHint.hide()
            self.mTabControl.show()
            if script != self.mTempScript:
                self.mTabControl.addTab(self.mTabHistory, QIcon(), '歷史紀錄')
            self.mTabControl.addTab(self.mTabScriptSetting, QIcon(), '設定')
            self.mLabelTitle.setText(script.Name)
            self.mTextScriptName.setText(script.Name)
            self.mSwitchEnable.setChecked(script.Enable)
            self.mScheduleSecond.setCurrentIndex(0 if not script.Schedule.mSecond else script.Schedule.mSecond[0])
            self.mScheduleMinute.setCurrentIndex(60 if not script.Schedule.mMinute else script.Schedule.mMinute[0])
            self.mScheduleHour.setCurrentIndex(24 if not script.Schedule.mHour else script.Schedule.mHour[0])
            self.mScheduleDays.setCurrentIndex(31 if not script.Schedule.mDays else script.Schedule.mDays[0]-1)
            self.mScheduleMonth.setCurrentIndex(12 if not script.Schedule.mMonth else script.Schedule.mMonth[0]-1)
            self.mLabelHistoryTitle.setText('')
            self.mLabelHistoryDesc.setText('')
            self.mTextHistoryContent.setPlainText('')
            self.mContainer.show()
            self.ReloadScriptModule()
            self.ReloadScriptHistory(script)
    
    def ReloadScriptHistory(self, script: NotifyScript):
        self.mTableHistory.setSortingEnabled(False)
        self.mTableHistory.setRowCount(0)
        for i, record in enumerate(script.Records):
            self.mTableHistory.insertRow(i)
            items = (
                QTableWidgetItem(' '),
                QTableWidgetItem(str(record.UpdateTime)),
                QTableWidgetItem(str(record.Title)),
                QTableWidgetItem(str(record.Description)),
            )
            items[0].setData(Qt.UserRole, (script, record))
            if not record.IsRead:
                items[0].setText('  ')
                items[0].setIcon(Resource.GetIcon('notification', 16))
            for j in range(1, len(items)):
                items[j].setToolTip(items[j].text())
            for j in range(len(items)):
                self.mTableHistory.setItem(i, j, items[j])
        self.mTableHistory.setSortingEnabled(True)
        self.mTableHistory.sortByColumn(1, Qt.SortOrder.DescendingOrder)
        self.mTableHistory.sortByColumn(0, Qt.SortOrder.DescendingOrder)
    
    def ReloadScriptModule(self):
        self.mComboScript.clear()
        self.mComboScript.addItem('無')
        for module in Resource.ListScriptPaths():
            self.mComboScript.addItem(module)
        if self.mCurrentScript.Context:
            for i in range(self.mComboScript.count()):
                if os.path.split(self.mCurrentScript.Context.Name)[1] == self.mComboScript.itemText(i):
                    self.mComboScript.setCurrentIndex(i)
                    break

    def ReloadScriptList(self, scripts: Dict[str, NotifyScript]):
        for i in range(self.mMenuScriptLayout.count()):
            self.mMenuScriptLayout.itemAt(0).widget().setParent(None)
        scriptList = [*scripts.values()]
        scriptList.sort(reverse=True, key=lambda x: x.Enable)
        for s in scriptList:
            records = s.Records
            btn = self._CreateScriptButton(s.Name)
            unread = list(filter(lambda x: not x.IsRead, records))
            btn.setIcon(Resource.GetIcon('notification' if unread else 'clock' if s.Enable else 'forward', 16))
            btn.clicked.connect(functools.partial(self._OnScriptButtonClicked, btn, s))
            btn.setProperty('enable', s.Enable)
            if s == self.mCurrentScript:
                btn.setProperty('active', True)
            self.mMenuScriptLayout.addWidget(btn)
        
        # show add script hint
        if not scriptList:
            widget = QWidget()
            widget.setObjectName('menu-hint')
            widget.setStyleSheet(Resource.GetQss('menu-hint', id='menu-hint', image='img/menu-hint.png'))
            widget.setFixedHeight(200)
            self.mMenuScriptLayout.addWidget(widget)
    
    # Events
    def _OnChangeTab(self, index: int):
        self.mBtnSaveScript.hide()
        self.mBtnDeleteScript.hide()
        self.mBtnReadAll.hide()
        self.mBtnReloadRecord.hide()
        if self.mTabControl.currentWidget() == self.mTabHistory:
            self.mBtnReadAll.show()
            self.mBtnReloadRecord.show()
            self.ReloadScriptHistory(self.mCurrentScript)
        elif self.mTabControl.currentWidget() == self.mTabScriptSetting:
            self.mBtnSaveScript.show()
        self.mBtnDeleteScript.show()

    def _OnReloadScriptHistory(self):
        if not self.mCurrentScript:
            return
        self.ReloadScriptHistory(self.mCurrentScript)

    def _OnReadAllRecord(self):
        record: NotifyRecord 
        if not self.mCurrentScript:
            return
        unread = []
        for row in range(self.mTableHistory.rowCount()):
            rowItem = self.mTableHistory.item(row, 0)
            script, record = rowItem.data(Qt.UserRole)
            if not record.IsRead:
                unread.append(record)

        if not unread:
            self.Msgbox('全部讀取', '沒有需要已讀的資訊')
            return

        if MB.No == self.Msgbox('全部讀取', '確定要全部已讀嗎？', MB.Yes | MB.No):
            return

        for record in unread:
            record.IsRead = True

        if self.RecordReadAll:
            self.RecordReadAll(self.mCurrentScript, unread)

        self.ReloadScriptHistory(self.mCurrentScript)
        self.Msgbox('全部讀取', '全部讀取完畢')

    def _OnScriptButtonClicked(self, sender: QPushButton, script: NotifyScript):
        # reload style
        for i in range(self.mMenuScriptLayout.count()):
            w = self.mMenuScriptLayout.itemAt(i).widget()
            w.setProperty('active', False)
            w.style().unpolish(w)
            w.style().polish(w)
        sender.setProperty('active', True)
        sender.style().unpolish(sender)
        sender.style().polish(sender)

        # check if edit or create
        if self.CheckNewScriptSave():
            self.OnLoadScriptDetails(script)
    
    def _OnHistoryChange(self, item: QTableWidgetItem):
        record: NotifyRecord 
        if not item:
            return
        row = item.row()
        rowItem = self.mTableHistory.item(row, 0)
        script, record = rowItem.data(Qt.UserRole)
        record.IsRead = True
        if self.RecordRead:
            self.RecordRead(script, record)
        rowItem.setIcon(QIcon())
        self.mLabelHistoryTitle.setText(record.Title)
        self.mLabelHistoryDesc.setText(record.Description)
        self.mTextHistoryContent.setPlainText(record.Content)
        self.mTextHistoryContent.show()
    
    def _OnRemoveScript(self):
        if not self.mCurrentScript:
            return
        if self.mTempScript:
            if MB.Yes == self.Msgbox('確認', '確定要捨棄新腳本 "{}" 嗎？'.format(self.mCurrentScript.Name), MB.Yes | MB.No, MB.Warning):
                self.mTempScript = None
                self.mCurrentScript = None
                self.ReloadScript()
        else:
            if MB.Yes == self.Msgbox('確認', '確定要刪除腳本 "{}" 嗎？'.format(self.mCurrentScript.Name), MB.Yes | MB.No, MB.Warning):
                self.mCurrentScript.Enable = False
                if self.ScriptRemove:
                    self.ScriptRemove(self.mCurrentScript)
                del self.mScripts[self.mCurrentScript.Name]
                self.mCurrentScript = None
                self.ReloadScriptList(self.mScripts)
                self.ReloadScript()

    def _OnAddScript(self):
        if not self.CheckNewScriptSave():
            return
        defaultName = '腳本{}'
        i = 1
        while defaultName.format(i) in self.mScripts:
            i += 1
        script = NotifyScript(defaultName.format(i))
        self.mTempScript = script
        self.OnLoadScriptDetails(script)

    def _OnSaveScript(self):
        enable = self.mSwitchEnable.isChecked()
        month  = None if self.mScheduleMonth.currentIndex() in (-1, 12) else (self.mScheduleMonth.currentIndex()+1)
        days   = None if self.mScheduleDays.currentIndex() in (-1, 31) else (self.mScheduleDays.currentIndex()+1)
        hour   = None if self.mScheduleHour.currentIndex() in (-1, 24) else self.mScheduleHour.currentIndex()
        minute = None if self.mScheduleMinute.currentIndex() in (-1, 60) else self.mScheduleMinute.currentIndex()
        second = None if self.mScheduleSecond.currentIndex() in (-1, 60) else self.mScheduleSecond.currentIndex()
        schedule = ScheduleTime(second, minute, hour, days, month)
        moduleIndex = self.mComboScript.currentIndex()
        moduleName = self.mComboScript.currentText()
        newName = self.mTextScriptName.text()
        oldName = self.mLabelTitle.text()

        if not newName:
            self.Msgbox('錯誤', '請輸入腳本名稱', icon = MB.Critical)
            return

        if (oldName != newName or self.mTempScript) and newName in self.mScripts:
            self.Msgbox('錯誤', '腳本名稱 "{}" 已存在'.format(newName), icon = MB.Critical)
            return

        if self.mTempScript != None:
            if MB.Yes == self.Msgbox('確認', '確定要新增腳本 "{}" 嗎？'.format(newName), MB.Yes | MB.No, MB.Information):
                self.mTempScript.Enable = enable
                self.mTempScript.Name = newName
                self.mTempScript.Schedule = schedule
                self.mTempScript.Context = ScriptContext(Resource.GetScriptPath(moduleName)) if moduleIndex else None
                self.mTempScript.Enable = enable
                self.mScripts[self.mTempScript.Name] = self.mTempScript
                if self.ScriptCreated:
                    self.ScriptCreated(self.mTempScript)
                self.mTempScript = None
        else:
            script: NotifyScript
            script = self.mScripts[oldName]

            if MB.Yes == self.Msgbox('確認', '確定要修改腳本 "{}" 嗎？'.format(oldName), MB.Yes | MB.No, MB.Information):
                if oldName != newName:
                    del self.mScripts[oldName]
                script.Enable = enable
                script.Name = newName
                script.Schedule = schedule
                script.Context = ScriptContext(Resource.GetScriptPath(moduleName)) if moduleIndex else None
                script.Enable = enable
                if oldName != newName:
                    self.mScripts[newName] = script
                if self.ScriptModified:
                    self.ScriptModified(script, oldName)
        self.ReloadScriptList(self.mScripts)
        self.ReloadScript()

    def _OnOpenScriptDirector(self):
        scriptDir = os.path.abspath(Resource.GetScriptPath(''))
        QDesktopServices.openUrl('file:///{}'.format(scriptDir))
    
    def _OnReloadScriptModules(self):
        self.ReloadScriptModule()

    # Virtual Function
    def closeEvent(self, event: QCloseEvent):
        self.hide()
        if self.ManagerHidden:
            self.ManagerHidden()
        event.ignore()