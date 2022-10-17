@echo off
rmdir /s build
git clone --branch master https://github.com/tomvandeneede/waarnemingenBEQuiz build
set PATH=%PATH%;c:\mingw\bin;%userprofiel%\go\bin\windows_386
set GOARCH=386
set GOOS=windows
set CGO_ENABLED=1
cd build
rem go build -o ../Roofvogels.exe
fyne package -os windows -icon icon.png
cd ..