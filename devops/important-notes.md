# Important Notes

## Python virtual environment

- Packages installed after activating `.venv` stay inside that `.venv`.
- `deactivate` only stops using the environment; it does not delete its packages.
- Activate it again with `source .venv/bin/activate`.
- Deleting `.venv` deletes all packages installed inside it.
- Recreate them with:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Use `which python` to verify that Python is coming from `.venv`.
