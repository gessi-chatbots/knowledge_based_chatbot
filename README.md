# Knowledge Based Chatbot
Knowledge based chatbot to find apps with desired features. Currently working on a small subset of applications. To adapt this chatbot simply follow the structure in the corresponding knowledge base file and re-train the model. 

## Description
Uses JSON files to provide knowledge base to the chatbot. Using the Rasa interface this chatbot allows smart user-machine interaction. This chatbot allows user to select a distinct application based on their preferred features.

## Sample Story -- find app by features
````
Your input ->  hello                                                                   
Hello! I am a mobile app assistant. Which features do you need help with?
Your input ->  I want to activate GPS Navigation                                       
Sure! I see you have multiple apps with this feature:
1. OsmAnd 
2. Organic Maps 
Do you wish to use any app in particular?
Your input ->  Whichever has Real-time traffic                                         
Great! Then let's launch OsmAnd!

````

## Sample Story -- Generate 
````
Your input -> hello                                                             
Hello! I am a mobile app assistant. Which features do you need help with?
Your input ->  I want to create a calendar event for my route
Let's get started! The following information is required:
  - start date/time
  - end date/time
  - invites
  - name
  - description
Please provide the 'start date/time':
Your input ->  August 25th
Please provide the 'end date/time':
Your input ->  August 26th
Please provide the 'invites':
Your input ->  ccg.campas@gmail.com
Please provide the 'name':
Your input -> Route Event
Please provide the 'description':
Your input -> If sunny we go on a hike!
Thank you got your information!
Please confirm the following is correct:
  - start date/time: August 25th
  - end date/time: August 26th
  - invites: ccg.campas@gmail.com
  - name: Route Event
  - description: If sunny we go on a hike!
````

## File structure

- \actions
  - ActionQueryKnowledgeBase.py: base actions that can be done using the current knowledge base
  - actions.py: actions that our chatbot can 
  - KnowledgeBase.py: Connection with our knowledge based used to extract and manipulate data from it.
  - EventHandler.py: Class controls input requirements from user for feature integrations between two different types.
  - Attention: obtains the attention on input for disambiguation of types
- \components
  - DateComponent: Detects dates in messages (including 'today', 'tomorrow', etc.) and standardizes date format
  - EmailComponent: Detects emails in messages using regex
  - FuzzyWuzzyComponent: custom components used within the chatbot, current FuzzyWuzzyComponent used to identify synonyms and correct spelling errors
- \data
  - nlu.yml: Training data stores structured information about user messages.
  - rules.yml: Training data used to train the chatbots dialogue management model, short pieces of conversations that should always follow the same path.
  - stories.yml: Training data used to train the chatbots dialogue management model, can be used to train models that are able to generalize to unseen conversation paths.
- \models: contains all currently trained models
- \scripts
  - json-to-nlu.py: Convert JSON (rasa_knowledge_base.json) file to NLU file that the chatbot can train with.
  - nltk_data.py: Download required NLTK package.
  - proactive-bot.py: Starts conversation with rasa chatbot externally.
- \test_python: scripts to generate tests with current data (specifically date tests)
- \tests
  - test_stories.yml: validate and test dialogues end-to-end by running through test stories
  - test_data_component.yml: test correct function of date identification component
  - test_email_component.yml: test correct function of email identification component
  - test_fuzzywuzzy_component.yml: test correct function of fuzzywuzzy component (input spelling errors fixed).
- \
  - config.yml: defines the components and policies that your model will use to make predictions based on user input.
  - credentials.yml: credentials for the Rasa X channel
  - domain.yml: universe in which the chatbot operates. It specifies the intents, entities, slots, responses, forms, and actions the bot should knows about. It also defines a configuration for conversation sessions.
  - endpoint.yml: contains the different endpoints the bot can use
  - markers.yml: conditions used to describe and mark points of interest in dialogues.
  - rasa_knowledge_base.json: knowledge based to be used by our chatbot

## Used technologies

Libraries, frameworks, engines, tools, third-party services...

| Component | Description | Version |
|--------------------------|------|---------|
|rasa|Open source framework for NLU, dialogue, and integrations.|>=3.0.0|
|fuzzywuzzy|uses Levenshtein Distance to calculate the differences between sequences in a simple-to-use package|0.2.0|
|NLTK|provides easy-to-use interfaces to over 50 corpora and lexical resources|3.6.6|
|re|Python regex library||
|datefinder|Finding and reformatting input dates||

## How to install
1. Install Rasa [https://rasa.com/docs/rasa/installation/]
3. Clone project
4. Enjoy!

## How to use
1. Enter _rasa train_ to train new model
2. Enter _rasa run_ to interact with chatbot externally
3. Enjoy!

## How to use (from CLI)
1. Enter _rasa train_ to train new model
2. Enter _rasa shell_ to interact with chatbot from CLI
3. Enjoy!

## How to use alongside chatbot_client
1. Enter _rasa run --enable-api --cors "*"_
2. Run chatbot client
3. Enjoy!

## Notes for developers

Check this for more information on rasa:
- https://github.com/RasaHQ/rasa/blob/main/docs/docs/command-line-interface.mdx

## License

Free use of this software is granted under the terms of the GNU General Public License v3.0: https://www.gnu.org/licenses/gpl.html
