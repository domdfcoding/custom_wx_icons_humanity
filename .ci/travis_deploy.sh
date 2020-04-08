if [ $TRAVIS_PYTHON_VERSION == "3.6" ]; then

  if [ -z "$TRAVIS_TAG" ]; then
      echo "Skipping deploy because this is not a tagged commit"

  else
      echo "Deploying to PyPI..."
      pip3 install twine
      twine upload  -u DomDF -p ${pypi_password} --skip-existing dist/*.whl

  fi

else
  echo "Skipping deploy because this is not the required Python version"

fi