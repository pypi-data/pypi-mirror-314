# Develop from the command line with cmake

This project requires:

* C++
* cmake
* ninja
* Python (can be installed with `uv`)
* Qt6

## venv preset

This preset uses the *Python* version installed in `.venv` with:

```bash
uv sync
```

### Workflow (configure, build, test)

```bash
cmake --workflow --preset venv
```

### Configure

```bash
cmake --preset venv
```

### (Re)compile

```bash
cmake --preset venv --build
```

### Run the C++ tests

```bash
ctest --preset venv
```

### Artifacts

The build artifacts are stored under `build/venv`.

#### Removing old artifacts

```bash
rm -rf build/venv
```
