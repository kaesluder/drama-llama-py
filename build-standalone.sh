#!/usr/bin/env sh

echo "This is a very rough build script, use with caution."

PROJECT_DIR=`pwd`

echo "Set PROJECT_DIR to:  $PROJECT_DIR"

source $PROJECT_DIR/venv/bin/activate

pyinstaller -w -F --add-data "gui:gui" $PROJECT_DIR/drama_llama.py 