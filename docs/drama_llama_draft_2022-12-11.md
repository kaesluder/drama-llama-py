# Drama Llama (Working Title) - Kae Job Sluder

## Team members (Leave blank for none)

* Document Theme Song [[We Don't Need This] Fascist Groove Thang (Extended Mix)](https://www.youtube.com/watch?v=sg2m7Qk2jdU)

## Problem Statement #1

The problem with someone's wrong on the internet anger is that someone is *always* wrong on the internet. (Sometimes it's you.)

Using the internet requires carefully curating or filtering through abundant low-quality content. Some of the issues include: 

* Opinion pieces presented as factual news
* Low-research articles
* Overgeneralization from hot-takes
* Self-promotional material
* Meta-controversy about what someone else said on the internet about something that happened on the internet
* Explicit prejudice and harassment 
* [Context collapse](https://en.wikipedia.org/wiki/Context_collapse) 

Attempts by large social media companies to develop a centralized response to
biased, inflammatory, and misleading information has become mired in political
controversy. On top of that, those responses have become limited by a business
model that monetizes user clicks and data about user clicks. Algorithmic views
of information reinforce user behavior, especially when user behavior is
addictive or compulsive. An evening of "doomscrolling" can bias the algorithm 
to presenting more of the same content, with trivial differences in information from article to article and post to post. 

Drama Llama is a curation- and filter-first newsreader. Users can build filters
using keyword, regex, and trainable natural language processing (NLP) tools.
This app will apply the same strategies used to detect email spam to helping
users curate, summarize, and tag individual articles or posts. The user can
choose to display this metadata at the headline level or use it to filter views. 

## MVP Feature Set

1.  RSS fetching and viewing
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
4.  Filter wizard
    - Drama Llama can suggest filters based on common patterns. 
### Potential Additional Features

1.  Machine Learning tagging using existing models
2.  Cross-platform testing
3.  Additional API and RSS integration

## Draft Technology Choices

- Front end: Electron or Browser using localStorage or indexedDB
- [Natural](https://github.com/NaturalNode/natural) (JS) provides tools for
  basic language processing including statistical classification algorithms
- Multiple machine learning/AI models exist for this kind of thing, more
  research is needed
- SQLite or other embedded data-storage solution
- JavaScript or Typescript depending on level of support
- React + css framework. 

## Additional content, diagrams, wireframes, user flows, etc.

[Early wireframes](Drama_Llama_Wireframes.pdf)