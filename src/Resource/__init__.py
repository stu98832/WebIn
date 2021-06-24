''' Project Resource Module '''

import os
import os.path
from typing import TextIO
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QFile, QIODevice
from PySide2.QtGui import QIcon

QT_UI_LOADER            = QUiLoader()
RESOURCE_LOCATION       = 'resources'
SCRIPT_FILE_LOCATION    = 'scripts'
EXTENSION_FILE_LOCATION = 'extensions'
UI_FILE_LOCATION        = "{path}.ui"
ICON_FILE_LOCATION      = 'icons/{size}x{size}/{path}.png'
ICONNEW_FILE_LOCATION   = 'icons-new/{path}.png'
QSS_FILE_LOCATION       = 'styles/{path}.qss'

def GetExtensionPath():
    ''' Get path of script package extending directory '''

    return os.path.join(EXTENSION_FILE_LOCATION).replace('\\', '/')

def GetQss(path: str, **params):
    ''' Get QSS string from .qss file, allow custom parameters '''

    paths = os.path.join(RESOURCE_LOCATION, QSS_FILE_LOCATION).format(path = path).replace('\\', '/')
    if not 'Resource' in params:
        params['Resource'] = RESOURCE_LOCATION
    qss = ''
    try:
        with open(paths, 'r', encoding='utf8') as f:
            f: TextIO
            qss = f.read()
    except:
        print('can not find style "{}"'.format(paths))
    for key, value in params.items():
        var = '@{}'.format(key)
        qss = qss.replace(var, str(value))
    return qss

def GetLocation(absolute = False):
    ''' Get relative location of resource, also can get absolute location '''

    return os.path.abspath(RESOURCE_LOCATION).replace('\\', '/') if absolute else RESOURCE_LOCATION

def GetScriptPath(scriptName=''):
    ''' Get script file path, empty repersent path of script directory '''

    paths = os.path.join(SCRIPT_FILE_LOCATION, scriptName).replace('\\', '/')
    return paths

def ListScriptPaths():
    ''' List all available script file in script directory '''

    paths = os.listdir(os.path.join(SCRIPT_FILE_LOCATION).replace('\\', '/'))
    paths = list(filter(lambda x: x.endswith('.py'), paths))
    return paths

def GetUI(name: str) -> QWidget:
    ''' loading QWidget by Qt from .ui file in resource directory. '''

    f = QFile(os.path.join(RESOURCE_LOCATION, UI_FILE_LOCATION).replace('\\', '/').format(path = name))
    if not f.open(QIODevice.ReadOnly):
        raise RuntimeError("無法載入 ui 檔案 {}: {}".format(f, f.errorString()))
    ui = QT_UI_LOADER.load(f)
    f.close()
    return ui

def GetIcon(name, size=32) -> QIcon:
    ''' Get QIcon from resource directory '''

    path = os.path.join(RESOURCE_LOCATION, ICON_FILE_LOCATION).replace('\\', '/').format(size = size, path = name)
    if os.path.exists(path):
        return QIcon(path)
    else:
        # TODO: Add Error log
        return QIcon()

def GetIconNew(name, size=32) -> QIcon:
    ''' Get QIcon from resource directory '''

    path = os.path.join(RESOURCE_LOCATION, ICONNEW_FILE_LOCATION).replace('\\', '/').format(size = size, path = name)
    if os.path.exists(path):
        return QIcon(path)
    else:
        # TODO: Add Error log
        return QIcon()