@echo off
setlocal

rem ############################################################################
rem #
rem # Release alphalens-cn to pypi
rem # Usage:
rem #   scripts\release.bat
rem #
rem # Note:
rem #   build & twine must be available in the venv
rem ############################################################################

set CURR_DIR=%~dp0
set REPO_ROOT=%CURR_DIR%..
call %CURR_DIR%_utils.bat

:main
echo.
echo ########################################
echo # Releasing *alphalens-cn*
echo ########################################

cd /d %REPO_ROOT%
echo.
echo ########################################
echo # pwd: %cd%
echo ########################################

echo.
echo ########################################
echo # Proceed?
echo ########################################
pause >nul

echo.
echo ########################################
echo # Building alphalens-cn
echo ########################################
python -m build

echo.
echo ########################################
echo # Release alphalens-cn to pypi
echo ########################################
pause >nul
python -m twine upload --repository pypi %REPO_ROOT%\dist\*

endlocal
