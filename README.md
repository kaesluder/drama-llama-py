# Drama Llama

## An experiment in feed reading and natural language processing.

### Project Background and Status

**This is a code bootcamp project in-progress!**

This is my final project for [Ada Developers Academy](https://adadevelopersacademy.org/). You can check out the [project prospectus](https://kaesluder.github.io/kae-garden-wiki/Ada_Capstone_Documentation/drama_llama_draft_2022-12-11/) for full details. Current goals are:

1.  RSS fetching and viewing _(80% complete)_
    - RSS is an XML standard for providing website, article, and post summaries.
      While many sites have moved away from RSS, it's still widely used.
2.  Keyword or regex tagging
    - Simple search on feed content.
3.  Natural Language Processing (NLP) tags
    - The first prototype will use very basic NLP algorithms such as Sentiment
      Analysis, Naive Bayesian Analysis, and/or Logistic Regression to tag text.
      These filters can be trained via user curation, and offer reasonable
      accuracy without extensive machine learning.
4.  Desktop app or desktop browser app
    - I think this will be challenging enough without trying to adapt to small-screen controls.
5.  Filter wizard
    - Drama Llama can suggest filters based on common patterns.

This project is _not_ at all usable at this point. Currently it consists of a python back end (this repo) and a react front end.

### Packages

Latest packages for M1 Mac can be found under [releases](https://github.com/kaesluder/drama-llama-py/releases/tag/v0.2.0-alpha). The zip archive includes a MacOS .app bundle and a console launcher. Linux build scripts are a work in progress.

### Experimental Run Instructions

For bash or zsh:

```sh
git clone https://github.com/kaesluder/drama-llama-py

# Note: sparse downloads do not work.

cd drama-llama-py
sh ./build.sh

# build app bundle
sh ./build-standalone.sh

# run desktop app without a full build
sh ./build.sh
sh ./run-llama.sh
```

If you want to run the GUI in a browser:

```sh
sh ./build.sh
source venv/bin/activate
flask run &
open ./gui/index.html
```

### Dependencies

#### Python

Developed using Python 3.10.9.

```
feedparser
pywebview
Flask
Flask-Cors
pyinstaller
pytest
```

[Pywebview](https://pywebview.flowrl.com/) has its own system requirements for different operating systems.

#### Javascript

```
react (v. 18)
axios
material-ui
luxon
jest
```
