from unittest import TestCase
from Core.Script.ScriptContext import ScriptContext

class TestScriptContext(TestCase):
    def test_NotFound(self):
        self.assertRaises(FileNotFoundError, ScriptContext, 'Tests/Core/ScriptTest-None.py')

    def test_SetGlobalVariable(self):
        ctx = ScriptContext('Tests/Core/ScriptTest.py')
        ctx.SetGlobalVariable('func', lambda x: x)
        self.assertEqual(ctx.Call('func', 1), 1)

    def test_GetGlobalVariable(self):
        ctx = ScriptContext('Tests/Core/ScriptTest.py')
        ctx.SetGlobalVariable('a', 32)
        self.assertEqual(ctx.GetGlobalVariable('a'), 32)