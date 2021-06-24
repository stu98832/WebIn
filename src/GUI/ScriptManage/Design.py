import os
from GUI import ScriptManage
from PySide2.QtGui import QDesktopServices, QFont, QIcon, QImage, QImageReader, QPicture
from PySide2.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QMessageBox,
    QMessageBox as MB,
    QPlainTextEdit,
    QScrollArea,
    QSplitter,
    QTabWidget,
    QTableWidget,
    QVBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
    QSizePolicy,
)
from PySide2.QtCore import QMargins, QSize, Qt
import Resource

class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self._InitializeComponent()
        self.show()

    def _InitializeComponent(self):
        inherit: 'ScriptManage.Form'
        inherit = self

        # Logo
        self.mLogo = QLabel()
        self.mLogo.setStyleSheet(Resource.GetQss('logo'))
        self.mLogo.setText('Web!n')
        self.mLogo.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.mLogo.setFont(QFont('Segoe UI', 18, QFont.Bold))
        self.mLogo.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.mLogo.setFixedHeight(50)

        # BtnAddScript
        self.mBtnAddScript = QPushButton()
        self.mBtnAddScript.setStyleSheet(Resource.GetQss('btn-add-script'))
        self.mBtnAddScript.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.mBtnAddScript.setFixedHeight(50)
        self.mBtnAddScript.setToolTip('新增腳本')
        self.mBtnAddScript.clicked.connect(inherit._OnAddScript)

        # BtnOption
        self.mBtnOption = QPushButton()
        self.mBtnOption.setStyleSheet(Resource.GetQss('btn-option'))
        self.mBtnOption.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.mBtnOption.setFixedHeight(50)
        self.mBtnOption.setToolTip('設定')
        self.mBtnOption.setIconSize(QSize(24, 24))
        self.mBtnOption.setIcon(Resource.GetIcon('slider', 24))

        # MenuScript
        self.mMenuScriptLayout = QVBoxLayout()
        self.mMenuScriptLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.mMenuScriptLayout.setSpacing(0)
        self.mMenuScript = QWidget()
        self.mMenuScript.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.mMenuScript.setLayout(self.mMenuScriptLayout)

        # MenuContainer
        self.mMenuContainer = QScrollArea()
        self.mMenuContainer.setStyleSheet(Resource.GetQss('menu-container'))
        self.mMenuContainer.setWidgetResizable(True)
        self.mMenuContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mMenuContainer.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.mMenuContainer.setWidget(self.mMenuScript)


        # Sidebar
        self.mSideberLayout = QVBoxLayout()
        self.mSideberLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.mSideberLayout.setSpacing(0)
        self.mSideberLayout.addWidget(self.mLogo)
        self.mSideberLayout.addWidget(self.mBtnAddScript)
        self.mSideberLayout.addWidget(self.mMenuContainer)
        # self.mSideberLayout.addWidget(self.mBtnOption)
        self.mSidebar = QWidget()
        self.mSidebar.setObjectName('sideber')
        self.mSidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.mSidebar.setFixedWidth(200)
        self.mSidebar.setStyleSheet(Resource.GetQss('sidebar', id = 'sidebar'))
        self.mSidebar.setLayout(self.mSideberLayout)

        # LabelTitle
        self.mLabelTitle = QLabel()
        self.mLabelTitle.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.mLabelTitle.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.mLabelTitle.setMinimumWidth(300)
        self.mLabelTitle.setFont(QFont('微軟正黑體', 20, QFont.Bold))

        # BtnReloadRecord
        self.mBtnReloadRecord = QPushButton()
        self.mBtnReloadRecord.setStyleSheet(Resource.GetQss('btn-primary', ButtonIcon='reload'))
        self.mBtnReloadRecord.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.mBtnReloadRecord.setFixedWidth(50)
        self.mBtnReloadRecord.setToolTip('重新整理')
        self.mBtnReloadRecord.clicked.connect(inherit._OnReloadScriptHistory)
        self.mBtnReloadRecord.hide()

        # BtnReadAll
        self.mBtnReadAll = QPushButton()
        self.mBtnReadAll.setStyleSheet(Resource.GetQss('btn-primary', ButtonIcon='read-all'))
        self.mBtnReadAll.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.mBtnReadAll.setFixedWidth(50)
        self.mBtnReadAll.setToolTip('全部讀取')
        self.mBtnReadAll.clicked.connect(inherit._OnReadAllRecord)
        self.mBtnReadAll.hide()

        # BtnSaveScript
        self.mBtnSaveScript = QPushButton()
        self.mBtnSaveScript.setStyleSheet(Resource.GetQss('btn-primary', ButtonIcon='save'))
        self.mBtnSaveScript.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.mBtnSaveScript.setFixedWidth(50)
        self.mBtnSaveScript.setToolTip('儲存腳本')
        self.mBtnSaveScript.clicked.connect(inherit._OnSaveScript)
        self.mBtnSaveScript.hide()

        # BtnDeleteScript
        self.mBtnDeleteScript = QPushButton()
        self.mBtnDeleteScript.setStyleSheet(Resource.GetQss('btn-del-script'))
        self.mBtnDeleteScript.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.mBtnDeleteScript.setFixedWidth(50)
        self.mBtnDeleteScript.setToolTip('刪除腳本')
        self.mBtnDeleteScript.clicked.connect(inherit._OnRemoveScript)
        self.mBtnDeleteScript.hide()

        # Navbar
        self.NavbarLayout = QHBoxLayout()
        self.NavbarLayout.setContentsMargins(QMargins(20, 0, 0, 1))
        self.NavbarLayout.setSpacing(0)
        self.NavbarLayout.addWidget(self.mLabelTitle)
        self.NavbarLayout.addWidget(self.mBtnReloadRecord)
        self.NavbarLayout.addWidget(self.mBtnReadAll)
        self.NavbarLayout.addWidget(self.mBtnSaveScript)
        self.NavbarLayout.addWidget(self.mBtnDeleteScript)
        self.mNavbar = QWidget()
        self.mNavbar.setObjectName('navbar')
        self.mNavbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.mNavbar.setStyleSheet(Resource.GetQss('navbar', id = 'navbar'))
        self.mNavbar.setFixedHeight(50)
        self.mNavbar.setLayout(self.NavbarLayout)

        # TableHistory
        self.mTableHistory = QTableWidget(0, 4)
        self.mTableHistory.setFont(QFont('微軟正黑體', 12))
        self.mTableHistory.setFrameStyle(QFrame.NoFrame)
        self.mTableHistory.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.mTableHistory.setStyleSheet('border-bottom: 1px solid rgb(192, 192, 192)')
        self.mTableHistory.setHorizontalHeaderLabels(['', '接收日期', '主旨', '描述'])
        self.mTableHistory.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.mTableHistory.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.mTableHistory.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.mTableHistory.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.mTableHistory.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.mTableHistory.horizontalHeader().setStretchLastSection(True)
        self.mTableHistory.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.mTableHistory.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.mTableHistory.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.mTableHistory.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.mTableHistory.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.mTableHistory.setShowGrid(False)
        self.mTableHistory.setColumnWidth(0, 16)
        self.mTableHistory.verticalHeader().setVisible(False)
        self.mTableHistory.itemClicked.connect(inherit._OnHistoryChange)

        # LabelHistoryTitle
        self.mLabelHistoryTitle = QLabel()
        self.mLabelHistoryTitle.setFont(QFont('微軟正黑體', 12))

        # LabelHistoryDesc
        self.mLabelHistoryDesc = QLabel()
        self.mLabelHistoryDesc.setFont(QFont('微軟正黑體', 12))
        self.mLabelHistoryDesc.setWordWrap(True)

        # TextHistoryContent
        self.mTextHistoryContent = QPlainTextEdit()
        self.mTextHistoryContent.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.mTextHistoryContent.setFont(QFont('微軟正黑體', 12))
        self.mTextHistoryContent.setStyleSheet(Resource.GetQss('history-content'))
        self.mTextHistoryContent.setReadOnly(True)
        self.mTextHistoryContent.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # HistoryDetailsWidget
        self.mHistoryDetailLayout = QVBoxLayout()
        self.mHistoryDetailLayout.setContentsMargins(QMargins(6, 6, 6, 6))
        self.mHistoryDetailLayout.setSpacing(6)
        self.mHistoryDetailLayout.addWidget(self.mLabelHistoryTitle)
        self.mHistoryDetailLayout.addWidget(self.mLabelHistoryDesc)
        self.mHistoryDetailLayout.addWidget(self.mTextHistoryContent)
        self.mHistoryDetailWidget = QWidget()
        self.mHistoryDetailWidget.setLayout(self.mHistoryDetailLayout)

        # TabHistory
        self.mSpliter = QSplitter()
        self.mSpliter.setOrientation(Qt.Orientation.Vertical)
        self.mSpliter.addWidget(self.mTableHistory)
        self.mSpliter.addWidget(self.mHistoryDetailWidget)
        self.mSpliter.setHandleWidth(8)
        self.mSpliter.handle(1).setAttribute(Qt.WA_Hover, True)
        self.mTabHistoryLayout = QVBoxLayout()
        self.mTabHistoryLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.mTabHistoryLayout.setSpacing(0)
        self.mTabHistoryLayout.addWidget(self.mSpliter)
        self.mTabHistory = QWidget()
        self.mTabHistory.setLayout(self.mTabHistoryLayout)

        # Label
        self.mLabel1 = QLabel('腳本名稱')
        self.mLabel1.setFont(QFont('微軟正黑體', 12))

        # TextScriptName
        self.mTextScriptName = QLineEdit()
        self.mTextScriptName.setFont(QFont('微軟正黑體', 12))

        # groupInfo
        self.mLayout1 = QHBoxLayout()
        self.mLayout1.addWidget(self.mLabel1)
        self.mLayout1.addWidget(self.mTextScriptName)
        self.mGroupInfoLayout = QVBoxLayout()
        self.mGroupInfoLayout.addLayout(self.mLayout1)
        self.mGroupInfoLayout.addStretch()
        self.mGroupInfo = QGroupBox('資訊')
        self.mGroupInfo.setLayout(self.mGroupInfoLayout)
        self.mGroupInfo.setFont(QFont('微軟正黑體', 16))

        # BtnOpenScriptDir
        self.mBtnOpenScriptDir = QPushButton('腳本資料夾')
        self.mBtnOpenScriptDir.setFont(QFont('微軟正黑體', 12))
        self.mBtnOpenScriptDir.clicked.connect(inherit._OnOpenScriptDirector)

        # BtnReloadScriptList
        self.mBtnReloadScriptList = QPushButton('重新載入')
        self.mBtnReloadScriptList.setFont(QFont('微軟正黑體', 12))
        self.mBtnReloadScriptList.clicked.connect(inherit._OnReloadScriptModules)

        # ComboScrit
        self.mComboScript = QComboBox()
        self.mComboScript.setFont(QFont('微軟正黑體', 12))
        self.mComboScript.addItem('無')

        # groupScript
        self.mLayout2 = QHBoxLayout()
        self.mLayout2.addWidget(self.mBtnOpenScriptDir)
        self.mLayout2.addWidget(self.mBtnReloadScriptList)
        self.mGroupScriptLayout = QVBoxLayout()
        self.mGroupScriptLayout.addLayout(self.mLayout2)
        self.mGroupScriptLayout.addWidget(self.mComboScript)
        self.mGroupScriptLayout.addStretch()
        self.mGroupScript = QGroupBox('腳本')
        self.mGroupScript.setLayout(self.mGroupScriptLayout)
        self.mGroupScript.setFont(QFont('微軟正黑體', 16))

        # label
        self.mLabel2 = QLabel('啟用')
        self.mLabel2.setFont(QFont('微軟正黑體', 12))

        # SwitchEnable
        self.mSwitchEnable = QCheckBox()
        self.mSwitchEnable.setChecked(True)

        # ScheduleMonth
        self.mScheduleMonth = QComboBox()
        self.mScheduleMonth.setFont(QFont('微軟正黑體', 12))
        self.mScheduleMonth.addItems(['{}月'.format(x+1) for x in range(12)])
        self.mScheduleMonth.addItem('每月')
        self.mScheduleMonth.setCurrentIndex(12)

        # ScheduleDay
        self.mScheduleDays = QComboBox()
        self.mScheduleDays.setFont(QFont('微軟正黑體', 12))
        self.mScheduleDays.addItems(['{}日'.format(x+1) for x in range(31)])
        self.mScheduleDays.addItem('每日')
        self.mScheduleDays.setCurrentIndex(31)

        # ScheduleHour
        self.mScheduleHour = QComboBox()
        self.mScheduleHour.setFont(QFont('微軟正黑體', 12))
        self.mScheduleHour.addItems(['{}時'.format(x) for x in range(24)])
        self.mScheduleHour.addItem('每小時')
        self.mScheduleHour.setCurrentIndex(24)

        # ScheduleMinute
        self.mScheduleMinute = QComboBox()
        self.mScheduleMinute.setFont(QFont('微軟正黑體', 12))
        self.mScheduleMinute.addItems(['{}分'.format(x) for x in range(60)])
        self.mScheduleMinute.addItem('每分鐘')
        self.mScheduleMinute.setCurrentIndex(60)

        # ScheduleSecond
        self.mScheduleSecond = QComboBox()
        self.mScheduleSecond.setFont(QFont('微軟正黑體', 12))
        self.mScheduleSecond.addItems(['{}秒'.format(x) for x in range(60)])
        self.mScheduleSecond.setCurrentIndex(0)

        # groupSchedule
        self.mLayout3 = QHBoxLayout()
        self.mLayout3.addWidget(self.mLabel2)
        self.mLayout3.addWidget(self.mSwitchEnable)
        self.mLayout3.addStretch()
        scheduleGroup = QHBoxLayout()
        scheduleGroup.addWidget(self.mScheduleMonth)
        scheduleGroup.addWidget(self.mScheduleDays)
        scheduleGroup.addWidget(self.mScheduleHour)
        scheduleGroup.addWidget(self.mScheduleMinute)
        scheduleGroup.addWidget(self.mScheduleSecond)
        self.GroupScheduleLayout = QVBoxLayout()
        self.GroupScheduleLayout.addLayout(self.mLayout3)
        self.GroupScheduleLayout.addLayout(scheduleGroup)
        self.GroupScheduleLayout.addStretch()
        self.mGroupSchedule = QGroupBox('排程')
        self.mGroupSchedule.setLayout(self.GroupScheduleLayout)
        self.mGroupSchedule.setFont(QFont('微軟正黑體', 16))

        # TabScriptSetting
        self.mTabScriptSettingLayout = QVBoxLayout()
        self.mTabScriptSettingLayout.setSpacing(0)
        self.mTabScriptSettingLayout.addWidget(self.mGroupInfo)
        self.mTabScriptSettingLayout.addWidget(self.mGroupScript)
        self.mTabScriptSettingLayout.addWidget(self.mGroupSchedule)
        self.mTabScriptSetting = QWidget()
        self.mTabScriptSetting.setObjectName('tabScriptSetting')
        self.mTabScriptSetting.setStyleSheet(Resource.GetQss('tab-script-setting', id = 'tabScriptSetting'))
        self.mTabScriptSetting.setLayout(self.mTabScriptSettingLayout)

        # tabControl
        self.mTabControl = QTabWidget()
        self.mTabControl.setStyleSheet(Resource.GetQss('tab-control'))
        self.mTabControl.setFont(QFont('微軟正黑體', 12))
        self.mTabControl.setVisible(False)
        self.mTabControl.currentChanged.connect(inherit._OnChangeTab)

        # ContentHint
        self.mContentHint = QWidget()
        self.mContentHint.setObjectName('content-hint')
        self.mContentHint.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mContentHint.setStyleSheet(Resource.GetQss('content-hint', 
            id = 'content-hint',
            image = 'img/central-hint.png'))

        # Content
        self.mContentLayout = QGridLayout()
        self.mContentLayout.setSpacing(0)
        self.mContentLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.mContentLayout.addWidget(self.mTabControl)
        self.mContentLayout.addWidget(self.mContentHint)
        self.mContentWidget = QWidget()
        self.mContentWidget.setLayout(self.mContentLayout)

        # Container
        self.mContainerLayout = QVBoxLayout()
        self.mContainerLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.mContainerLayout.setSpacing(0)
        self.mContainerLayout.addWidget(self.mNavbar)
        self.mContainerLayout.addWidget(self.mContentWidget)
        self.mContainer = QWidget()
        self.mContainer.setObjectName('container')
        self.mContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.mContainer.setStyleSheet(Resource.GetQss('container', id = 'container'))
        self.mContainer.setLayout(self.mContainerLayout)

        # MainWindow
        self.mMainLayout = QHBoxLayout()
        self.mMainLayout.addWidget(self.mSidebar)
        self.mMainLayout.addWidget(self.mContainer)
        self.mMainLayout.setContentsMargins(QMargins(0, 1, 0, 0))
        self.mMainLayout.setSpacing(1)
        self.mCentralWidget = QWidget()
        self.mCentralWidget.setObjectName('main')
        self.mCentralWidget.setStyleSheet(Resource.GetQss('main', id = 'main'))
        self.mCentralWidget.setLayout(self.mMainLayout)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setMinimumSize(800, 600)
        self.resize(1024, 768)
        self.setCentralWidget(self.mCentralWidget)
        self.setWindowTitle('WebIn')
        self.setWindowIcon(Resource.GetIconNew('favicon'))

    def Msgbox(self, title, msg, btns = MB.Ok, icon = QMessageBox.Icon.NoIcon):
        msgbox = QMessageBox()
        msgbox.setWindowTitle(title)
        msgbox.setIcon(icon)
        msgbox.setText(msg)
        msgbox.setStandardButtons(btns)
        return msgbox.exec_()

    def _CreateScriptButton(self, name):
        btn = QPushButton(name)
        btn.setFont(QFont('微軟正黑體', 12))
        btn.setMinimumHeight(50)
        btn.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        btn.setToolTip(name)
        btn.setProperty('active', False)
        return btn
