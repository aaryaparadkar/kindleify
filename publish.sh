#!/bin/bash
# Kindleify publish script - Push to PyPI
# Usage: ./publish.sh [test]

set -e

cd "$(dirname "$0")"

echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

echo "Building package..."
uv run pyproject-build

if [ "$1" == "test" ]; then
    echo "Uploading to Test PyPI..."
    uv run twine upload --repository testpypi dist/*
    echo "Uploaded to https://test.pypi.org/"
else
    echo "Uploading to PyPI..."
    uv run twine upload dist/*
    echo "Uploaded to https://pypi.org/project/kindleify/"
fi

echo "Done!"