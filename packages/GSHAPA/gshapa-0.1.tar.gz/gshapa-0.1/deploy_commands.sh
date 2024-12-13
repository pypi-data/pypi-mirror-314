# Run the setup and build the package
python setup.py sdist bdist_wheel
# Upload the package to pypi repository
#twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
twine upload --repository pypi dist/*
