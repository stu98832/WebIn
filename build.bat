@echo off

echo Clean dist directory...
rmdir /S /Q dist > nul 1> nul

echo Start build...
pyinstaller --name="WebIN" --windowed --onefile src\main.py --icon resources\icons-new\favicon.ico
IF ERRORLEVEL 1 GOTO FAILED

echo Copy resources...
xcopy /Y /E /I resources dist\resources > nul

echo Copy scripts...
xcopy /Y /E /I scripts dist\scripts > nul

echo Copy extensions...
xcopy /Y /E /I extensions dist\extensions > nul

:SUCCESS
echo Build success.
pause
exit /b 0

:FAILED
echo Fail to build. code: %ERRORLEVEL%
pause
exit /b 1