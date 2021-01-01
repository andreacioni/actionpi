#!/bin/bash

#echo "Testing app"...
#python3 -m pytest ./tests

echo "Check if checkout on master"
CURRENT_BRANCH=$(git rev-parse --symbolic-full-name --abbrev-ref HEAD)

echo "Current branch is: $CURRENT_BRANCH"
if [ $CURRENT_BRANCH != "master" ]; then
    echo "Not checked out master, aborting..."
    exit 1
fi

#echo "Updating pypi tools..."
#python3 -m pip install --user --upgrade setuptools wheel twine

echo "Cleaning temp directories..."
rm -rf build/ dist/ pycommon_andreacioni.egg-info/

echo "Creating new version"
FILE=setup.py
CURRENT_VERSION=$(cat $FILE | grep version | awk '{print $1}' | cut -d '"' -f 2)
TO_UPDATE=(
    setup.py
    actionpi/app.py
)

echo "Current version is: $CURRENT_VERSION. Enter new version:"
read NEW_VERSION
echo "New version is: $NEW_VERSION"

for file in "${TO_UPDATE[@]}"
do
    echo "Patching $file ..."
    sed -i '' "s/$CURRENT_VERSION/$NEW_VERSION/g" $file
    git add $file
done

git commit -m "Releasing v$NEW_VERSION"
git push
git tag -a v$NEW_VERSION -m "Release v$NEW_VERSION"
git push origin v$NEW_VERSION

#echo "Creating version for PyPi"
#python3 setup.py sdist bdist_wheel

#echo "Uploading to PyPi"
#python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*