from queue import Queue
from typing import List
from PySide2.QtCore import (
    QObject,
    Signal, 
    Slot)
from GUI.NotifyWidget import NotifyWidget
import App

class NotifyManager(QObject):
    ''' Notify Widgets Manager '''

    mNotifySlot: List[NotifyWidget]
    mPending: "Queue[NotifyWidget]"

    mSigPush = Signal(str, str)
    
    def __init__(self, app: 'App.NotifyApp', maxsize: int = 3, lifetime: float = 15.0):
        super().__init__()
        self.mApp = app
        self.mMaxNotifySize = maxsize
        self.mLifeTime      = lifetime
        self.mNotifySlot    = [None]*maxsize
        self.mPending       = Queue()
        self.mSigPush.connect(self._PushNotify)
    
    def Clear(self):
        for i in range(self.mMaxNotifySize):
            self.mNotifySlot[i] = None
        while not self.mPending.empty():
            self.mPending.get()

    def PushNotify(self, title: str, desc: str):
        self.mSigPush.emit(title, desc)
    
    def _CalculatePosition(self, widget: NotifyWidget, index: int):
        ''' Calculate new position of NotiftWidget '''

        screen = self.mApp.primaryScreen().availableGeometry()
        size = widget.Size()
        x, y  = screen.width()-size.width(), screen.height()-(size.height()+2)*index-10
        return x, y

    @Slot(str, str)
    def _PushNotify(self, title, desc):
        ''' Push an NotiftWidget with title and description, Widget will in wait state if all slots are occupied '''

        widget = NotifyWidget(self, title, desc, self.mLifeTime)

        # Select suitable slot for Widget
        for i in range(self.mMaxNotifySize):
            if self.mNotifySlot[i] == None:
                widget.Show(*self._CalculatePosition(widget, i+1))
                self.mNotifySlot[i] = widget
                return

        # Waiting for slot if all slot are occupied
        self.mPending.put(widget)

    def _AdjustNotify(self):
        ''' Adjust positions of all NotifyWidget when some slot are empty '''

        j = 0
        for i in range(self.mMaxNotifySize):
            if self.mNotifySlot[i] != None: 
                if i != j:
                    self.mNotifySlot[j] = self.mNotifySlot[i]
                    self.mNotifySlot[j].Move(*self._CalculatePosition(self.mNotifySlot[j], j+1))
                    self.mNotifySlot[i] = None
                j += 1

    @Slot(QObject)
    def _DestroyNotify(self, widget):
        '''  Destroy Notify Widget '''

        if not widget in self.mNotifySlot:
            return

        index = self.mNotifySlot.index(widget)
        self.mNotifySlot[index] = None

        # Insert Widget when there have any available Widget in pending queue
        # Otherwise Adjest positions of NotifyWidget
        if self.mPending.qsize()> 0:
            widget = self.mPending.get()
            widget.Show(*self._CalculatePosition(widget, index+1))
            self.mNotifySlot[index] = widget
        else:
            self._AdjustNotify()