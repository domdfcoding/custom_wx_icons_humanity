#!/bin/bash
# Script for building sdist and bdist_wheel for all themes
# To build additional themes just add them to the list below

rm -rf dist
mkdir dist

for theme in adwaita hicolor humanity suru tango
do
  echo ''
  echo "Building $theme icon theme"
  cd $theme || continue

  # Check if inkscape is available
  if which inkscape; then
    # Build icons from source if required
    if test -f build_icons_from_src.py; then
      echo "Building icons from svg source files"
      python3 build_icons_from_src.py || exit
    fi
  fi

  # Build
  echo "Building source and wheel distributions"
  python3 setup.py sdist bdist_wheel || exit

  # Copy built files
  echo "Copying source and wheel distributions to ./dist"
  cp dist/* ../dist/ || exit

  # Cleanup
  rm -rf dist
  rm -rf build
  rm -rf *.egg-info

  cd ..
done