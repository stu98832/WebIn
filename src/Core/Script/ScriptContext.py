import os
import sys
import importlib.util

class ScriptContext:
    def __init__(self, filename: str):
        self.Name = filename
        self._LoadScriptFile(filename)

    def SetGlobalVariable(self, name: str, value):
        setattr(self.mModule, name, value)
    
    def GetGlobalVariable(self, name: str):
        return getattr(self.mModule, name, None)

    def Call(self, name: str, *args):
        return getattr(self.mModule, name)(*args)

    def _LoadScriptFile(self, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError('找不到腳本檔案: {}'.format(os.path.abspath(filename)))

        spec = importlib.util.spec_from_file_location('Context', filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.mModule = module