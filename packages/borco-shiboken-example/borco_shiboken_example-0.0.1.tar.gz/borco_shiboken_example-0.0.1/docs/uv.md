# uv

## Compile and sync

```bash
uv sync
```

## Run the Python tests

```bash
pytest
```

or

```bash
uv run pytest
```

## Publish to pypi

```bash
rm -rf .venv/ build/ dist/
```

```bash
uv sync
```

```bash
uv build
```

```bash
uv publish
```
