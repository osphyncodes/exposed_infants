@echo off
REM Set MySQL base and data directories
SET BASEDIR=C:\Users\Ngomba_joseph\mysql
SET DATADIR=%BASEDIR%\data

REM Go to the MySQL bin directory
cd /d %BASEDIR%\bin

echo Starting MySQL Server...
mysqld --console --basedir=%BASEDIR% --datadir=%DATADIR%

pause
REM Note: Ensure that the MySQL server is properly installed and configured.
REM This script assumes that the MySQL server is installed in C:\Users\Ngomba_joseph\mysql
REM Adjust the BASEDIR and DATADIR variables as necessary to match your installation.