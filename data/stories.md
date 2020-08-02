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

## General thank you

* Thank you
    - utter_youre_welcome

## What is your work scedule 

* When do you work
    - utter_Im_always_here

## Who made you
* Who made you?
-utter_who_made_you

## Introduction: name,bot,who made you, what can you do

* Bot_introduction
    - utter_my_name_is_newt
* bot_challenge
    - utter_iamabot
* Who made you?
    - utter_who_made_you
* What can you do
    - utter_what_can_you_do

## Greet to what type of questions

* greet
    - utter_greet
* mood_great
    - utter_happy
* Got Question
    - utter_got_question
* What type of questions?
    - utter_what_types_of_question_can_you_answer

## Question plus whats the source

* nutrition_definition{"nutrient_regex":"חלבון"}
    - action_simple_question
* What is the source of your data
    - utter_source_of_your_data
