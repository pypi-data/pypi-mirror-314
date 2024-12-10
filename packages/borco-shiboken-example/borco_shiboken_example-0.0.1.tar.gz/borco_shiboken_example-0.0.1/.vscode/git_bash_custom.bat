@set PATH=%USERPROFILE%\scoop\apps\python\current\Scripts;%USERPROFILE%\scoop\apps\python\current;%USERPROFILE%\scoop\shims;%PATH%
@call "%QTENV2_BAT%"
@call "%VCVARSALL_BAT%" %*
@call pushd %WORKSPACE_FOLDER%

@set VENV_ACTIVATE=%WORKSPACE_FOLDER%\.venv\Scripts\activate.bat
if exist %VENV_ACTIVATE% (
    @echo Activating .venv ...
    @call %VENV_ACTIVATE%
) else (
    @echo Local Python .venv not found. Create one with "uv sync".
)

"%GIT_BASH%" --login -i
