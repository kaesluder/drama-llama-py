#!/usr/bin/env sh

echo "This is a very rough build script, use with caution."

PROJECT_DIR=`pwd`

echo "Set PROJECT_DIR to:  $PROJECT_DIR"

echo "Downloading front end."

git subtree add --prefix gui-src https://github.com/kaesluder/drama-llama-react.git main --squash

echo "Creating local virtual environment."

python3 -m venv venv
source $PROJECT_DIR/venv/bin/activate

echo `which pip`

echo 

echo "Installing python dependencies. "

pip install -r $PROJECT_DIR/requirements.txt

echo

echo "Installing react dependencies. "
cd $PROJECT_DIR/gui-src
yarn 
yarn build

echo "Moving compiled JavaScript to ./gui"
cd $PROJECT_DIR
cp -r $PROJECT_DIR/gui-src/build $PROJECT_DIR/gui

