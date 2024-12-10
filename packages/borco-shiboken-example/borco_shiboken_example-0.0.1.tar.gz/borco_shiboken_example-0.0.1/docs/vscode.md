# VS Code

## "Git Bash (Custom)" VSCode terminal profile

If you use *VSCode*, the workspace is configured to use a custom terminal that:

* loads `vcvarsall.bat` to configure *Visual Studio* C++ toolchain
* loads `qtenv2.bat` to configure *Qt6*
* launches *git bash*

The custom terminal profile is named `Git Bash (Custom)`.

The profile name, the locations of `vcvarsall.bat` and `qtenv2.bat`, along with
other variables are defined in `.vscode/settings.json`.

When creating the terminal, *VSCode* executes `.vscode/git_bash_custom.bat`,
passing it the `env` defined in `.vscode/settings.json`.
