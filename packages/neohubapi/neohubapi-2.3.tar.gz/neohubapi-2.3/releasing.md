# Making a new release

Bump version number in setup.txt

```
python3 setup.py bdist_wheel sdist
twine upload dist/*
git tag -s v${VERSION}
```
