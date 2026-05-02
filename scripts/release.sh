#!/bin/bash

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
  echo "Usage: ./scripts/release.sh <version>"
  exit 1
fi

echo "Releasing version $VERSION..."

# Clean
rm -rf dist build *.egg-info

# Build
python -m build

# Upload
twine upload dist/*

# Git tag
git add .
git commit -m "Release v$VERSION"
git tag v$VERSION
git push origin master --tags

echo "Release v$VERSION complete."