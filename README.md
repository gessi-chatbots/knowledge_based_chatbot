# Knowledge Based Chatbot

Brief summary

## Description

Extended summary: purpose, main components, technologies

## File structure

- \actions
  - ActionQueryKnowledgeBase.py:
  - actions.py:
  - customComponents.py:
  - KnowledgeBase.py:
- \data
  - nlu.yml
  - rules.yml
  - stories.yml
- \models: contains all currently trained models
- \scripts
  - json-to-nlu.py
  - nltk_data.py
  - proactive-bot.py
- \tests
  - test_stories.yml:
- \
  - config.yml: 
  - credentials.yml:
  - domain.yml:
  - endpoint.yml:
  - markers.yml:
  - rasa_knowledge_base.json

## Used technologies

Libraries, frameworks, engines, tools, third-party services...

| Component | Description | Version |
|--------------------------|------|---------|
|rasa|Open source framework for NLU, dialogue, and integrations.|>=3.0.0|
|fuzzywuzzy|uses Levenshtein Distance to calculate the differences between sequences in a simple-to-use package|0.2.0|

## How to install

1. Clone project
2. Run "install"
3. Enjoy!

## How to use

1. Run "use"
2. Enter parameters
3. Enjoy!

## Notes for developers

Check this for more information on rasa:
- https://github.com/RasaHQ/rasa/blob/main/docs/docs/command-line-interface.mdx

## License

Free use of this software is granted under the terms of the GNU General Public License v3.0: https://www.gnu.org/licenses/gpl.html
