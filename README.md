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

This project is _not_ at all usable at this point. Currently it consists of a python back end (this repo) and a separate [react GUI](https://github.com/kaesluder/drama-llama-react) that will be integrated into a single desktop app eventually.

### Experimental Run Instructions

In a separate shell. For bash or zsh:

```sh
git clone https://github.com/kaesluder/drama-llama-py
cd drama-llama-py
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

**You will also need the [python server](https://github.com/kaesluder/drama-llama-react)**. Using [yarn](https://yarnpkg.com/):

```sh
git clone https://github.com/kaesluder/drama-llama-react
cd drama-llama-react
yarn
yarn start # start the react interface on a simple web server.
```
