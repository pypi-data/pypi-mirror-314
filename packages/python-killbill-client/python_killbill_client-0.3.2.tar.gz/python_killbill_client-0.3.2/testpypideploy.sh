# Requirements
# python3 -m pip install --upgrade pip
# python3 -m pip install --upgrade build
# python3 -m pip install --upgrade twine

# Build
python3 -m build

# Upload to testpypi
python3 -m twine upload --repository testpypi dist/*

# Upload to pypi
# python3 -m twine upload dist/*

# Install
python3 -m pip install --index-url https://test.pypi.org/simple/ -U python-killbill-client 