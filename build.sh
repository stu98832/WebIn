#! /usr/bin/bash

echo "Clean dist directory..."
rm -r ./dist

pyinstaller --name="WebIN" --windowed --onefile ./src/main.py --icon resources/icons-new/favicon.ico

ERRCODE=$?
if [ ! $ERRCODE -eq 0 ] 
then
    echo "Fail to build. code: $ERRCODE"
    exit 1
fi

echo "Copy resources..."
cp -r ./src/resources dist/resources
ERRCODE=$?
if [ ! $ERRCODE -eq 0 ] 
then
    echo "Fail to build. code: $ERRCODE"
    exit 1
fi

echo "Copy scripts..."
cp -r ./src/scripts dist/scripts
ERRCODE=$?
if [ ! $ERRCODE -eq 0 ] 
then
    echo "Fail to build. code: $ERRCODE"
    exit 1
fi

echo "Copy extensions..."
cp -r ./src/extensions dist/extensions
ERRCODE=$?
if [ ! $ERRCODE -eq 0 ] 
then
    echo "Fail to build. code: $ERRCODE"
    exit 1
fi

echo "Build success."