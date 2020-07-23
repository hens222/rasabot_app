## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## nutrition definition
* nutrition_definition
  - action_nutrition_definition

## nutrition what has
* nutrition_what_has
  - action_nutrition_what_has

## nutrition importance
* nutrition_importance
  - action_nutrition_importance

## nutrition howmanyxiny
* nutrition_howmanyxiny
  - action_nutrition_howmanyxiny

## Whats your name short (1)

* Bot_introduction
    - utter_my_name_is_newt

## Whats your name longer (2)

* greet
    - utter_greet
* Bot_introduction
    - utter_my_name_is_newt

## Whats your name Longest (2)
* greet
    - utter_greet
* mood_great
    - utter_happy
* Bot_introduction
    - utter_my_name_is_newt

## I have a question
*Got Question
- utter_got_question

## What can you do

* What can you do
    - utter_what_can_you_do

## Bot introduction path 1

* greet
    - utter_greet
* Bot_introduction
    - utter_my_name_is_newt
* What can you do
    - utter_what_can_you_do

## Bot introduction path 2

* Bot_introduction
    - utter_my_name_is_newt
* What can you do
    - utter_what_can_you_do

## Greet and ask
* greet
    - utter_greet
* Got Question
    - utter_got_question

## What is the source of your data

* What is the source of your data
    - utter_source_of_your_data

## What is the source of your data

* What is the source of your data
    - utter_source_of_your_data

## Is OJ healthy story

* Is OJ healthy
    - utter_is_OJ_healthy

## happy path

* greet
    - utter_greet
* mood_great
    - utter_happy

## Question + thank you path

* Got Question
    - utter_got_question
* Thank you
    - utter_whats_your_question

## What type of questions

* What type of questions?
    - utter_what_types_of_question_can_you_answer

## Question + what type path

* Got Question
    - utter_got_question
* What type of questions?
    - utter_what_types_of_question_can_you_answer

## What type of story + ack path

* What type of questions?
    - utter_what_types_of_question_can_you_answer
* mood_great
    - utter_whats_your_question

## Got Question +a fffirm path

* Got Question
    - utter_got_question
* affirm
    - utter_whats_your_question

## Got questions + mood great path

* Got Question
    - utter_got_question
* mood_great
    - utter_whats_your_question

## Intro-question-which question

* Bot_introduction
    - utter_my_name_is_newt
* What can you do
    - utter_what_can_you_do
* What type of questions?
    - utter_what_types_of_question_can_you_answer
* Thank you
    - utter_whats_your_question

## Greet+unhappy+cheer+thank you

* greet
    - utter_greet
* mood_unhappy
    - utter_cheer_up
    - utter_did_that_help
* Thank you
    - utter_happy

## Nutrition tip

* Can you share nutrition tips
    - utter_nutrition_tips

## I want to be healthier

* I want to eat or be healthy
    - utter_I_wanna_be_healthier

## Whats good nutrition

* What is good nutrition
    - utter_whats_good_nutrition

## General thank you

* Thank you
    - utter_youre_welcome

## What is your work scedule 

* When do you work
    - utter_Im_always_here

## What to eat before training short 

* What should I eat before a training session
    - utter_which_type_of_exercise

## New Story

* What to eat before a run
    - utter_what_to_eat_before_aerobic_session

## New Story

* What should I eat before a training session
    - utter_which_type_of_exercise
* Aerobic training
    - utter_what_to_eat_before_aerobic_session

## What should I eat before an aerobic session long version

* What should I eat before a training session
    - utter_which_type_of_exercise
* Aerobic training
    - utter_what_to_eat_before_aerobic_session

## What to eat before strength conditioning

* What should I eat before a training session
    - utter_which_type_of_exercise
* Strength training
    - utter_what_to_eat_before_strength_training
