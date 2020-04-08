#!/bin/bash
# Script for building all themes
# To build additional themes just add them to the list below

rm -rf dist
mkdir dist

for theme in adwaita hicolor humanity suru tango
do
  cd $theme || continue

  # Build
  python3 setup.py sdist bdist_wheel || exit

  # Copy built files
  cp dist/* ../dist/ || exit

  # Cleanup
  rm -rf dist
  rm -rf build
  rm -rf *.egg-info

  cd ..
done