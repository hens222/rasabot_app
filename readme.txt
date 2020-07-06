References: 
- https://rasa.com/docs/rasa/user-guide/rasa-tutorial
- https://towardsdatascience.com/create-chatbot-using-rasa-part-1-67f68e89ddad
- https://medium.com/legobots/build-a-chatbot-with-rasa-stack-the-beginners-guide-bbb435af4111
- https://www.youtube.com/watch?v=VXvWdrr2yw8 --> 14:00-24:00

# ---------------------------------------------------------------------------------------------------------

(*) Schematic illustration for RASA flow:

               ---------------------------------------------------------------------
               | RASA                                                              |
               |    -----------------                           ----------------   |
               |    | Natural       |    Structured Data        | Core Model   |   |
    User       |    | Language      |    (Intents, Entities)    | (Dialogue    |   |
    Message ------->| Understanding |-------------------------->|  Management) |------> Respond
               |    | (NLU)         |     User's Stories ------>|              |   |    (Utter, Action, Event)
               |    -----------------     (pre-Trained)         ----------------   |
               |     "what the user                              "what the bot     | 
               |      will/may ask"                               will answer"     |
               ---------------------------------------------------------------------

    - RASA 1.0 merges NLU and CORE into a single product (previously were separated products).

    - RASA Flow:

        For every conversation that the user does with the bot, RASA NLU does intent classification 
        and entity extraction, and RASA Core is responsible for what Bot will “utter” to the user:


                     |----- NLU -----|------------ Core Model ------------|        
        Message In ---> Interpreter ---> Tracker ---> Policy ---> Action ---> Message Out
                            |               |            |
                        (Intent,      (Converstation  (Action
                         Entities)     State)          choice)

    - A story is a representation of a conversation between a user and an AI assistant, converted into a specific format where user inputs are
      expressed as corresponding intents (and entities where necessary) while the responses of an assistant are expressed as corresponding action names.

    - Stories can be spread across multiple files and specify the folder containing the files for most of the scripts (e.g. training, visualization).
      The stories will be treated as if they would have been part of one large file.

    - Additional info:  https://rasa.com/docs/rasa/core/stories/#stories

    - RASA supports multi-languages. For additional info, see: https://rasa.com/docs/rasa/nlu/language-support

# ---------------------------------------------------------------------------------------------------------

(*) Quick Start

    - Install Conda or MiniConda (https://docs.conda.io/en/latest/miniconda.html)

    % conda install python=3.6
    % conda create -n rasa python=3.6
    % source activate rasa
    % pip install rasa-x --extra-index-url https://pypi.rasa.com/simple

# ---------------------------------------------------------------------------------------------------------

(*) Create a new project:

    % rasa init --no-prompt

# ---------------------------------------------------------------------------------------------------------

(*) Important files:

    - domain.yml --------> Assistant’s domain, defines the supported intents and the corresponding actions and responses
    - data/nlu.md -------> NLU training data, mainly for Intent definitions
    - data/stories.md ---> Stories, defines the conversation flow
    - config.yml --------> NLU and Core Model Configuration, e.g. language, pipelines, policies, etc.
    - actions.py --------> Code for custom actions (custom python code)
    
    - models/<timestamp>.tar.gz ----> your initial model

    - credentials.yml ---> To connect other services like slack, facebook messanger, google voice assistant, etc.
    - endpoints.yml -----> To interact with the bot over REST API or for storing tracker information (conversations) on server

# ---------------------------------------------------------------------------------------------------------

(*) Training:

    % rasa train

    - Shall be called for updating (retraining) the NLU and the Core Model.
    - The updated model will be stored in models/ directory

# ---------------------------------------------------------------------------------------------------------

(*) Testings:

    % rasa test

    - End-to-end tests are defined in tests/ directory, ensure both NLU and Core make correct predictions.

    - Additional info:  https://rasa.com/docs/rasa/user-guide/testing-your-assistant

# ---------------------------------------------------------------------------------------------------------

(*) Launching locally:

    % rasa shell

# ---------------------------------------------------------------------------------------------------------

(*) RASA-X

    Rasa-X is a browser-based GUI tool which allows training machine-learning model by using GUI based interactive mode.
    It’s an optional tool in Rasa Software Stack. It aims to learn from real conversations and improve the bot.

    When running Rasa-X locally, all training data and stories are read from the files in the project (e.g. data/nlu.md), and any changes
    in the UI are saved back to those files. Conversations and other data are stored in an SQLite database saved in a file called rasa.db.

(*) Launching with RASA-X

    % rasa x

    Then open http://localhost:5002/talk

(*) Working with Custom Actions:

    - endpoints.yml --------------------> enable (uncomment) action_endpoint section
    - actions.py -----------------------> implement the custom action class
    - nlu.md, stories.md, domain.yml ---> register the new intent and corresponding action

    % rasa run actions --actions actions

    % rasa x --endpoints endpoints.yml

# ---------------------------------------------------------------------------------------------------------

(*) Deploy on Heroku using Docker:

    - https://medium.com/analytics-vidhya/deploying-rasa-chatbot-on-heroku-using-docker-7199bf16c219

