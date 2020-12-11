## Suprised
* suprised
  - utter_suprised

## Jokes
* jokes
  - utter_jokes

## Greet happy path
* greet
  - utter_greet
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"phone"}
* inform{"integer":"0501234567"}
    - profile_form
    - slot{"phone":"0501234567"}
    - slot{"requested_slot":"username"}
* inform{"name":"גיל"}
    - profile_form
    - slot{"username":"גיל"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
* inform{"integer":"38"}
    - profile_form
    - slot{"age":"38"}
    - slot{"requested_slot":"weight"}
* inform{"integer":"72"}
    - profile_form
    - slot{"weight":"72"}
    - slot{"requested_slot":"height"}
* inform{"integer":"172"}
    - profile_form
    - slot{"height":"172"}
    - slot{"requested_slot":null}
    - form{"name":null}

## Greet sad path
* greet
  - utter_greet
* deny
  - utter_identication_next_time

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

## nutrition howmanyxiny
* nutrition_howmanyxiny
  - action_nutrition_howmanyxiny

## nutrition and_what_about_x
* nutrition_and_what_about_x
  - action_nutrition_howmanyxiny

## nutrition is_food_healthy
* nutrition_is_food_healthy
  - action_nutrition_is_food_healthy

## nutrition what_is_healthier
* nutrition_what_is_healthier
  - action_nutrition_what_is_healthier

## nutrition is_food_recommended
* nutrition_is_food_recommended
  - action_nutrition_is_food_recommended

## nutrition get_rda
* nutrition_get_rda
  - action_nutrition_get_rda

## nutrition get_upper_limit
* nutrition_get_upper_limit
  - action_nutrition_get_rda

## nutrition bloodtest_generic_question
* nutrition_bloodtest_generic_question
  - action_nutrition_bloodtest_generic

## nutrition bloodtest_value_question
* nutrition_bloodtest_value_question
  - action_nutrition_bloodtest_value

## nutrition food_substitute_question
* nutrition_food_substitute_question
  - action_nutrition_food_substitute

## personlization list
* personlization_list
  - action_personlization_list

## personlization remove
* personlization_remove
  - action_personlization_remove
  - profile_form
  - form{"name": null}

## user information
* request_profile_info
  - profile_form
  - form{"name": "profile_form"}
  - form{"name": null}

## Introduction
* bot_introduction
  - utter_my_name_is_newt

## I have a question
* got_question
  - utter_got_question

## Question + thank you path
* got_question
  - utter_got_question
* thank_you
  - utter_whats_your_question

## what_type_of_questions
* what_type_of_questions
	- utter_what_can_you_do

## Question + what type path
* got_question
  - utter_got_question
* what_type_of_questions
  - utter_what_can_you_do

## What type of story + ack path
* what_type_of_questions
  - utter_what_can_you_do
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

## Question plus whats the source
* nutrition_definition
  - action_simple_question

## What to eat before X
* nutrition_what_to_eat_before
  - action_simple_question

## What to eat after X
* nutrition_what_to_eat_after
  - action_simple_question

## What impacts
* nutrition_what_impacts
  - action_simple_question

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

## Is food healthy with entity
* nutrition_is_food_healthy{"food_entity":"אגס"}
  - action_nutrition_is_food_healthy

## How much x in y, and then is y healty
* nutrition_howmanyxiny{"nutrient":"פוטסיום"}
  - action_nutrition_howmanyxiny
* nutrition_is_food_healthy{"food_entity":"עגבניה"}
  - action_nutrition_is_food_healthy

## Is healthy enhanced 
* nutrition_definition{"nutrition_concept":"קיטו"}
  - action_simple_question
* nutrition_is_healthy{"nutrition_concept":"קיטו"}
  - action_simple_question

## Is healthy story
* nutrition_is_healthy{"nutrition_concept":"צמחונות"}
  - action_simple_question

## Is healthy two kinds working great
* nutrition_is_healthy{"nutrition_concept":"צמחונות"}
  - action_simple_question
* nutrition_is_healthy{"nutrition_concept":"קיטו"}
  - action_simple_question
* nutrition_is_food_healthy{"food_entity":"לחם"}
  - action_nutrition_is_food_healthy
* nutrition_is_food_healthy{"food_entity":"תפוח עץ"}
  - action_nutrition_is_food_healthy

## What is healthier switch the foods
* nutrition_what_is_healthier{"food_entity":"חומוס","food_entity2":"טחינה"}
  - action_nutrition_what_is_healthier
* nutrition_what_is_healthier{"food_entity":"טחינה","food_entity2":"חומוס"}
  - action_nutrition_what_is_healthier

## Multiple what is healthier 3x
* nutrition_what_is_healthier{"food_entity":"חלב שקדים","food_entity2":"חלב סויה"}
  - action_nutrition_what_is_healthier
* nutrition_what_is_healthier{"food_entity":"חומוס","food_entity2":"טחינה"}
  - action_nutrition_what_is_healthier
* nutrition_what_is_healthier{"food_entity":"פיצה"}
  - action_nutrition_what_is_healthier

## Is healthy simple question
* nutrition_is_healthy
  - action_simple_question

## What doesnt have too much of X
* nutrition_what_has_little{"nutrient":"סוכר"}
  - action_simple_question

## What does not have X
* nutrition_what_has_little{"nutrient":"סוכר"}
  - action_simple_question

## What has little saturated fat
* nutrition_what_has_little{"nutrient":"שומן רווי"}
  - action_simple_question

## What can you do
* What can you do
    - utter_what_can_you_do

## Great Onboarding 1

* greet
    - utter_greet
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"phone"}
* inform{"integer":"0587100788"}
    - profile_form
    - slot{"age":null}
    - slot{"weight":null}
    - slot{"height":null}
    - slot{"phone":"0587100788"}
    - slot{"requested_slot":"username"}
* inform{"name":"גיל"}
    - profile_form
    - slot{"username":"גיל"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
* inform{"integer":"38"}
    - profile_form
    - slot{"phone":"0587100788"}
    - slot{"weight":null}
    - slot{"height":null}
    - slot{"age":"38"}
    - slot{"requested_slot":"weight"}
* inform{"integer":"73"}
    - profile_form
    - slot{"phone":"0587100788"}
    - slot{"age":"38"}
    - slot{"height":null}
    - slot{"weight":"73"}
    - slot{"requested_slot":"height"}
* inform{"integer":"182.5"}
    - profile_form
    - slot{"phone":"0587100788"}
    - slot{"age":"38"}
    - slot{"weight":"73"}
    - slot{"height":"182.5"}
    - form{"name":null}
    - slot{"requested_slot":null}

## Nutrition and what about X 2

* nutrition_howmanyxiny{"nutrient":"קלוריות"}
    - action_nutrition_howmanyxiny
    - slot{"x":"קלוריות"}
    - slot{"y":"קייל"}
* nutrition_and_what_about_x{"nutrient":"ברזל"}
    - action_nutrition_howmanyxiny
    - slot{"x":"ברזל"}
    - slot{"y":"קייל"}
* nutrition_howmanyxiny
    - action_nutrition_howmanyxiny
    - slot{"x":"ברזל"}
    - slot{"y":"ברוקולי"}

## Nutrition how to improve

* nutrition_howto_improve{"goal_or_state":"לרזות"}
    - action_simple_question

## Nutrition_howto_improve 2 

* nutrition_howto_improve{"goal_or_state":"לעלות מסת שריר"}
    - action_simple_question
* nutrition_howto_improve{"goal_or_state":"מערכת חיסונית"}
    - action_simple_question

## Nutrition_howto_improve 3 

* nutrition_howto_improve{"goal_or_state":"ריכוז"}
    - action_simple_question

## Nutrition_howto_improve multi goals

* nutrition_howto_improve{"goal_or_state":"רמת האנרגיה"}
    - action_simple_question
* nutrition_howto_improve{"goal_or_state":"מידת העייפות"}
    - action_simple_question
* nutrition_howto_improve{"goal_or_state":"להוריד כולסטרול"}
    - action_simple_question
* nutrition_howto_improve{"goal_or_state":"להעלות כולסטרול טוב"}
    - action_simple_question

## Get upper limit question 

* nutrition_get_upper_limit{"food_entity":"ביצים"}
    - action_nutrition_get_rda

## Get RDA plus upper limit

* nutrition_get_rda{"food_entity":"ביצים"}
    - action_nutrition_get_rda
* nutrition_get_upper_limit{"food_entity":"ביצים"}
    - action_nutrition_get_rda

## Nutrition bloodtest meanining 1

* nutrition_bloodtest_meaning{"nutrient":"טריגליצרידים"}
    - action_simple_question

## Nutrition bloodtest meaning 2

* nutrition_bloodtest_meaning{"nutrient":"LDL"}
    - action_simple_question

## Nutrition bloodtest what if too low 1

* nutrition_bloodtest_whatif_toolow{"nutrient":"ברזל"}
    - action_simple_question

## Food subs - beef 

* nutrition_food_substitute_question{"food_entity":"בקר"}
    - action_nutrition_food_substitute

## What to eat after 2 step

* nutrition_what_to_eat_after{"training_type":"אימון"}
    - action_simple_question
* nutrition_what_to_eat_after{"training_type":"אימון כדורסל"}
    - action_simple_question
