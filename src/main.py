import os
import sys
import ctypes
import ctypes.util
import PySide2
from App import NotifyApp
from PySide2 import QtXml
from PySide2 import QtCore
import Constants

if __name__ == '__main__':
    # 指定 Qt 插件的位置
    # 避免在 virtual environment 無法正常使用
    QTDir = os.path.dirname(PySide2.__file__) 
    QTPluginPath = os.path.join(QTDir, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = QTPluginPath
    os.chdir(Constants.ROOT_DIR)
    
    app = NotifyApp()
    app.Run()