Distribution requirements:
```
setuptools
wheel
```

Generate package with
```
python3 setup.py sdist bdist_wheel
```


Publish with
```
python3 -m twine upload  dist/* --verbose
```
