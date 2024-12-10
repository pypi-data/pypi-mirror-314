# Architect Log
The project will utilize industry best practices to structure ADRs, making them easy to reference and update as the system evolves.

```bash
pip freeze > requirements.txt

pip install .

rm -rf dist/* build/ src/architect_log.egg-info

python3 -m build

python3 -m twine upload --repository testpypi dist/*
```
