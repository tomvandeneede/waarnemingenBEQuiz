@echo off
rmdir /s build
git clone --branch master https://github.com/tomvandeneede/waarnemingenBEQuiz build
set PATH=%PATH%;c:\mingw\bin
set GOARCH=386
set GOOS=windows
set CGO_ENABLED=1
cd build
go build -o ../Roofvogels.exe
cd ..