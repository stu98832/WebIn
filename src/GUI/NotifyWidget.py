from PySide2.QtWidgets import (
    QLabel,
    QPushButton)

from PySide2.QtCore import (
    Qt, 
    QObject,
    QPropertyAnimation, 
    QPoint, 
    QTimer)

import Resource

class NotifyWidget(QObject):
    mButtonClose: QPushButton
    mLabelDesc: QLabel
    mLabelTitle: QLabel

    def __init__(self, manager, title, desc, lifetime=15.0):
        super().__init__()
        self.mManager = manager
        self.mTitle = title
        self.mDescription = desc
        self.mLiftTime = lifetime
        self._InitializeComponent()

    def _InitializeComponent(self):
        self.mTimer = QTimer()
        self.mTimer.setInterval(int(self.mLiftTime*1000))
        self.mTimer.timeout.connect(self.Destroy)

        self.mWidget = Resource.GetUI('notify')
        self.mWidget.setWindowFlags(
            Qt.Window | 
            Qt.FramelessWindowHint | 
            Qt.Tool | 
            Qt.WindowStaysOnTopHint)

        self.mLabelTitle  = self.mWidget.findChild(QLabel, 'lbTitle')
        self.mLabelTitle.setText(self.mTitle)

        self.mLabelDesc = self.mWidget.findChild(QLabel, 'lbDesc')
        self.mLabelDesc.setText(self.mDescription)

        self.mButtonClose = self.mWidget.findChild(QPushButton, 'btnClose') 
        self.mButtonClose.setIcon(Resource.GetIcon('multiply'))
        self.mButtonClose.clicked.connect(self.Hide)

        self.mDisappearAnimation = QPropertyAnimation(self.mWidget, b"windowOpacity")
        self.mDisappearAnimation.finished.connect(self.Destroy)
        self.mDisappearAnimation.setDuration(100)

        self.mOpacityAdimation = QPropertyAnimation(self.mWidget, b"windowOpacity")
        self.mOpacityAdimation.setDuration(200)

        self.mMoveAnimation = QPropertyAnimation(self.mWidget, b"pos")
        self.mMoveAnimation.setDuration(150)
    
    def Size(self):
        return self.mWidget.size()

    def Show(self, x: int, y: int):
        self.mWidget.setWindowOpacity(0.0)
        self.mWidget.move(x+self.mWidget.size().width(), y)
        self.mWidget.show()
        self.mWidget.clearFocus()

        self.mMoveAnimation.setEndValue(QPoint(x, y))
        self.mMoveAnimation.start()

        self.mOpacityAdimation.setEndValue(1.0)
        self.mOpacityAdimation.start()
        self.mTimer.start()

    def Move(self, x: int, y: int):
        self.mMoveAnimation.setEndValue(QPoint(x, y))
        self.mMoveAnimation.start()

    def Hide(self):
        if self.mWidget.isHidden():
            return

        if self.mTimer.isActive():
            self.mTimer.stop()

        self.mDisappearAnimation.setEndValue(0.0)
        self.mDisappearAnimation.start()

    def Destroy(self):
        self.mWidget.hide()
        self.mManager._DestroyNotify(self)