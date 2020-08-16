## Suprised
* suprised
  - utter_suprised

## Jokes
* jokes
  - utter_jokes

## Greet happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## Greet sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## say goodbye
* goodbye
  - utter_goodbye

## Bot challenge
* bot_challenge
  - utter_iamabot

## nutrition definition
* nutrition_definition
  - action_simple_question

## nutrition what has
* nutrition_what_has
  - action_simple_question

## nutrition importance
* nutrition_importance
  - action_simple_question

## nutrition howto improve
* nutrition_howto_improve
  - action_simple_question

## nutrition howmanyxiny
* nutrition_howmanyxiny
  - action_nutrition_howmanyxiny

## nutrition is_food_healthy
* nutrition_is_food_healthy
  - action_nutrition_is_food_healthy

## nutrition what_is_healthier
* nutrition_what_is_healthier
  - action_nutrition_what_is_healthier

## Whats your name short (1)
* bot_introduction
  - utter_my_name_is_newt
* nice_to_meet_you
  - slot{"username": "NA"}
  - utter_nice_to_meet_you

## Whats your name longer (2)
* greet
  - utter_greet
* bot_introduction
  - utter_my_name_is_newt
* nice_to_meet_you
  - slot{"username": "NA"}
  - utter_nice_to_meet_you

## Whats your name Longest (2)
* greet
  - utter_greet
* mood_great
  - utter_happy
* bot_introduction
  - utter_my_name_is_newt
* nice_to_meet_you
  - slot{"username": "NA"}
  - utter_nice_to_meet_you

## I have a question
* got_question
  - utter_got_question

## what_can_you_do
* what_can_you_do
  - utter_what_can_you_do

## Bot introduction path 1
* greet
  - utter_greet
* bot_introduction
  - utter_my_name_is_newt
* nice_to_meet_you
  - slot{"username": "NA"}
  - utter_nice_to_meet_you
* what_can_you_do
  - utter_what_can_you_do

## Bot introduction path 2
* bot_introduction
  - utter_my_name_is_newt
* nice_to_meet_you
  - slot{"username": "NA"}
  - utter_nice_to_meet_you
* what_can_you_do
  - utter_what_can_you_do

## Greet and ask
* greet
  - utter_greet
* got_question
  - utter_got_question

## what_is_the_source_of_your_data
* what_is_the_source_of_your_data
  - utter_source_of_your_data

## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## Question + thank you path
* got_question
  - utter_got_question
* thank_you
  - utter_whats_your_question

## what_type_of_questions
* what_type_of_questions
  - utter_what_types_of_question_can_you_answer

## Question + what type path
* got_question
  - utter_got_question
* what_type_of_questions
  - utter_what_types_of_question_can_you_answer

## What type of story + ack path
* what_type_of_questions
  - utter_what_types_of_question_can_you_answer
* mood_great
  - utter_whats_your_question

## got_question +a fffirm path
* got_question
  - utter_got_question
* affirm
  - utter_whats_your_question

## Got questions + mood great path
* got_question
  - utter_got_question
* mood_great
  - utter_whats_your_question

## Intro-question-which question
* bot_introduction
  - utter_my_name_is_newt
* nice_to_meet_you
  - slot{"username": "NA"}
  - utter_nice_to_meet_you
* what_can_you_do
  - utter_what_can_you_do
* what_type_of_questions
  - utter_what_types_of_question_can_you_answer
* thank_you
  - utter_whats_your_question

## Greet+unhappy+cheer+thank you
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* thank_you
  - utter_happy

## Nutrition tip
* can_you_share_nutrition_tips
  - utter_nutrition_tips

## I want to be healthier
* I_want_to_eat_or_be_healthy
  - utter_I_wanna_be_healthier

## General thank you
* thank_you
  - utter_youre_welcome

## What is your work scedule 
* when_do_you_work
  - utter_Im_always_here

## who_made_you
* who_made_you
  - utter_who_made_you

## Introduction: name,bot,who made you, what can you do
* bot_introduction
  - utter_my_name_is_newt
* nice_to_meet_you
  - slot{"username": "NA"}
  - utter_nice_to_meet_you
* bot_challenge
  - utter_iamabot
* who_made_you
  - utter_who_made_you
* what_can_you_do
  - utter_what_can_you_do

## Greet to what type of questions
* greet
  - utter_greet
* mood_great
  - utter_happy
* got_question
  - utter_got_question
* what_type_of_questions
  - utter_what_types_of_question_can_you_answer

## Question plus whats the source
* nutrition_definition
  - action_simple_question

## nutrition what_to_eat_before_training_short
* nutrition_what_to_eat_before
  - action_simple_question
* nutrition_training_type
  - slot{"training_type": "NA"}
  - action_eat_before_training

## nutrition what_to_eat_before_training_long
* nutrition_what_to_eat_before
  - action_simple_question
* nutrition_training_type
  - slot{"training_type": "NA"}
  - action_simple_question
  - utter_how_long_running
* nutrition_training_duration
  - slot{"training_duration": "NA"}
  - action_eat_before_training

## What to eat before X
* nutrition_what_to_eat_before
  - action_simple_question

## What to eat after X
* nutrition_what_to_eat_after
  - action_simple_question

## What impacts
* nutrition_what_impacts
  - action_simple_question

## Greet + got question
* greet
    - utter_greet
* Got Question
    - utter_got_question

## Should I avoid X?
* nutrition_should_I_avoid
    - action_simple_question

## Will X make me fat
* will_X_make_me_fat
    - utter_will_it_make_me_fat

## How much X in Y multiple questions
* nutrition_howmanyxiny{"nutrient":"קלוריות"}
    - action_nutrition_howmanyxiny
* nutrition_howmanyxiny{"nutrient":"חלבון"}
    - action_nutrition_howmanyxiny
* nutrition_howmanyxiny{"nutrient":"סודיום"}
    - action_nutrition_howmanyxiny
* thank_you
    - utter_youre_welcome

## Hi + many jokes
* greet
    - utter_greet
* mood_great
    - utter_happy
* jokes
    - utter_jokes
* jokes
    - utter_jokes
* jokes
    - utter_jokes

## Is food healthy with entity
* nutrition_is_food_healthy{"food_entity":"אגס"}
    - action_nutrition_is_food_healthy

## How much x in y, and then is y healty
* nutrition_howmanyxiny{"simple_entity":"פוטסיום"}
    - action_nutrition_howmanyxiny
* nutrition_is_food_healthy{"food_entity":"עגבניה"}
    - action_nutrition_is_food_healthy
