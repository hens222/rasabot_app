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

## nutrition is_food_recommended
* nutrition_is_food_recommended
  - action_nutrition_is_food_recommended

## nutrition get_rda
* nutrition_get_rda
  - action_nutrition_get_rda

## user information
* request_profile_info
  - profile_form
  - form{"name": "profile_form"}
  - form{"name": null}

## Whats your name short (short)
* bot_introduction
  - utter_my_name_is_newt
* slot_getter_username
  - slot{"username": "NA"}
  - utter_profile_info_getter
* deny
  - utter_slot_getter_username

## Whats your name short (long)
* bot_introduction
  - utter_my_name_is_newt
* slot_getter_username
  - slot{"username": "NA"}
  - utter_profile_info_getter
* affirm
  - profile_form
  - form{"name": "profile_form"}
  - form{"name": null}
  - utter_slot_getter_username

## I have a question
* got_question
  - utter_got_question

## what_can_you_do
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
* nutrition_what_has_little{"nutrient":"מדי סוכר"}
  - action_simple_question

## What does not have X
* nutrition_what_has_little{"nutrient":"סוכר"}
  - action_simple_question

## What has little saturated fat
* nutrition_what_has_little{"nutrient":"שומן רווי"}
  - action_simple_question

## Form 2
* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username{"username":"גיל"}
    - slot{"username":"גיל"}
    - slot{"username":"גיל"}
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
    - slot{"username":"גיל"}
* slot_getter_age{"age":"38"}
    - profile_form
    - slot{"age":"38"}
    - slot{"requested_slot":"weight"}
* slot_getter_weight{"weight":"72"}
    - profile_form
    - slot{"weight":"72"}
    - slot{"requested_slot":"height"}
* slot_getter_height{"height":"172"}
    - profile_form
    - slot{"height":"172"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username

## Form 4


* greet
    - utter_greet
* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username{"username":"גיל"}
    - slot{"username":"גיל"}
    - slot{"username":"גיל"}
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
    - slot{"username":"גיל"}
* slot_getter_age{"age":"38"}
    - profile_form
    - slot{"age":"38"}
    - slot{"requested_slot":"weight"}
* slot_getter_weight{"age":"72"}
    - profile_form
    - slot{"weight":"72"}
    - slot{"requested_slot":"height"}
    - slot{"username":"גיל"}
* slot_getter_height{"age":"182"}
    - profile_form
    - slot{"height":"182"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username

## Form 3

* greet
    - utter_greet
* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username{"username":"גיל"}
    - slot{"username":"גיל"}
    - slot{"username":"גיל"}
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
    - slot{"username":"גיל"}
* slot_getter_age{"age":"38.5"}
    - profile_form
    - slot{"age":"38.5"}
    - slot{"requested_slot":"weight"}
* slot_getter_weight{"weight":"72.3"}
    - profile_form
    - slot{"weight":"72.3"}
    - slot{"requested_slot":"height"}
    - slot{"username":"גיל"}
* slot_getter_height{"height":"182.2"}
    - profile_form
    - slot{"height":"182.2"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username

## Form 5

* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
* slot_getter_age{"weight":"37.5"}
    - profile_form
    - slot{"age":"37.5"}
    - slot{"requested_slot":"weight"}
* slot_getter_weight{"age":"82"}
    - profile_form
    - slot{"weight":"82"}
    - slot{"requested_slot":"height"}
* slot_getter_height{"age":"201"}
    - profile_form
    - slot{"height":"201"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username

## Form 1 plus RDA questions

* slot_getter_username{"username":"גיל"}
    - slot{"username":"גיל"}
    - slot{"username":"גיל"}
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
    - slot{"username":"גיל"}
* slot_getter_age{"age":"35.5"}
    - profile_form
    - slot{"age":"35.5"}
    - slot{"requested_slot":"weight"}
    - slot{"username":"גיל"}
* slot_getter_weight{"weight":"80.1"}
    - profile_form
    - slot{"weight":"80.1"}
    - slot{"requested_slot":"height"}
* slot_getter_height{"height":"175"}
    - profile_form
    - slot{"height":"175"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username
* nutrition_get_rda{"nutrient":"ברזל"}
    - action_nutrition_get_rda
* nutrition_get_rda{"nutrient":"ויטמין סי"}
    - action_nutrition_get_rda
* thank_you
    - utter_youre_welcome

## Form - Got name but deny details plus reply

* slot_getter_username{"username":"ליאור"}
    - slot{"username":"ליאור"}
    - slot{"username":"ליאור"}
    - utter_profile_info_getter
    - slot{"username":"ליאור"}
* deny
    - utter_slot_getter_username_deny_details

## Form 6

* slot_getter_username
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"נקבה"}
    - profile_form
    - slot{"gender":"נקבה"}
    - slot{"requested_slot":"age"}
* slot_getter_age{"weight":"19"}
    - profile_form
    - slot{"age":"19"}
    - slot{"requested_slot":"weight"}
* slot_getter_weight{"weight":"45"}
    - profile_form
    - slot{"weight":"45"}
    - slot{"requested_slot":"height"}
* slot_getter_height{"weight":"163"}
    - profile_form
    - slot{"height":"163"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username
* thank_you
    - utter_youre_welcome

## Form 7

* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username{"username":"רמון"}
    - slot{"username":"רמון"}
    - slot{"username":"רמון"}
    - utter_profile_info_getter
    - slot{"username":"רמון"}
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
    - slot{"username":"רמון"}
* slot_getter_age{"age":"49"}
    - profile_form
    - slot{"age":"49"}
    - slot{"requested_slot":"weight"}
* slot_getter_weight{"weight":"71"}
    - profile_form
    - slot{"weight":"71"}
    - slot{"requested_slot":"height"}
    - slot{"username":"רמון"}
* slot_getter_height{"height":"176"}
    - profile_form
    - slot{"height":"176"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username

## Form 8

* greet
    - utter_greet
* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
* slot_getter_age{"weight":"102"}
    - profile_form
    - slot{"age":"102"}
    - slot{"requested_slot":"weight"}
* slot_getter_weight{"weight":"89"}
    - profile_form
    - slot{"weight":"89"}
    - slot{"requested_slot":"height"}
* slot_getter_height{"weight":"169"}
    - profile_form
    - slot{"height":"169"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username

## Myname is X but deny details

* slot_getter_username{"username":"גיל"}
    - slot{"username":"גיל"}
    - utter_profile_info_getter
* deny
    - utter_slot_getter_username_deny_details

## Form 9

* slot_getter_username{"nutrient":"ונס"}
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
* slot_getter_age{"weight":"74"}
    - profile_form
    - slot{"age":"74"}
    - slot{"requested_slot":"weight"}
* slot_getter_weight{"weight":"121"}
    - profile_form
    - slot{"weight":"121"}
    - slot{"requested_slot":"height"}
* slot_getter_height{"weight":"169"}
    - profile_form
    - slot{"height":"169"}
    - form{"name":null}
    - slot{"requested_slot":null}

## Form 10

* greet
    - utter_greet
* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
* slot_getter_age{"age":"76"}
    - profile_form
    - slot{"age":"76"}
    - slot{"requested_slot":"weight"}
* slot_getter_weight{"weight":"82"}
    - profile_form
    - slot{"weight":"82"}
    - slot{"requested_slot":"height"}
* slot_getter_height{"height":"154"}
    - profile_form
    - slot{"height":"154"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username

## Form 11

* slot_getter_username
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"נקבה"}
    - profile_form
    - slot{"gender":"נקבה"}
    - slot{"requested_slot":"age"}
* slot_getter_age{"age":"28"}
    - profile_form
    - slot{"age":"28"}
    - slot{"requested_slot":"weight"}
* slot_getter_weight{"weight":"56"}
    - profile_form
    - slot{"weight":"56"}
    - slot{"requested_slot":"height"}
* slot_getter_height{"height":"162"}
    - profile_form
    - slot{"height":"162"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username

## Form 12

* greet
    - utter_greet
* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"נקבה"}
    - profile_form
    - slot{"gender":"נקבה"}
    - slot{"requested_slot":"age"}
* slot_getter_age{"age":"49"}
    - profile_form
    - slot{"age":"49"}
    - slot{"requested_slot":"weight"}
* slot_getter_weight{"weight":"67"}
    - profile_form
    - slot{"weight":"67"}
    - slot{"requested_slot":"height"}
* slot_getter_height{"height":"174"}
    - profile_form
    - slot{"height":"174"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username

## Form 13

* slot_getter_username
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
* slot_getter_age{"age":"53"}
    - profile_form
    - slot{"age":"53"}
    - slot{"requested_slot":"weight"}
* slot_getter_weight{"weight":"73"}
    - profile_form
    - slot{"weight":"73"}
    - slot{"requested_slot":"height"}
* slot_getter_height{"height":"191"}
    - profile_form
    - slot{"height":"191"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username

## Name intro 1

* greet
    - utter_greet
* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username
    - utter_profile_info_getter

## Name intro 2

* greet
    - utter_greet
* slot_getter_username
    - utter_profile_info_getter

## Name intro 3

* slot_getter_username{"username":"ארז"}
    - utter_profile_info_getter

## Name intro 4

* slot_getter_username{"username":"אבי"}
    - utter_profile_info_getter

## Name intro 5

* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username
    - utter_profile_info_getter

## Form 14

* greet
    - utter_greet
* affirm
    - utter_happy
* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username{"username":"טובה"}
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"נקבה"}
    - profile_form
    - slot{"gender":"נקבה"}
    - slot{"requested_slot":"age"}
* slot_getter_age{"age":"77"}
    - profile_form
    - slot{"age":"77"}
    - slot{"requested_slot":"weight"}
* slot_getter_weight{"weight":"95"}
    - profile_form
    - slot{"weight":"95"}
    - slot{"requested_slot":"height"}
* slot_getter_height{"height":"167"}
    - profile_form
    - slot{"height":"167"}
    - form{"name":"טובה"}
    - slot{"requested_slot":null}

## Form deny 2

* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username
    - utter_profile_info_getter
* deny
    - utter_slot_getter_username_deny_details

## Form 15

* greet
    - utter_greet
* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username{"username":"מיכה"}
    - slot{"username":"מיכה"}
    - slot{"username":"מיכה"}
    - utter_profile_info_getter
    - slot{"username":"מיכה"}
* affirm{"simple_entity":"בטח"}
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
    - slot{"username":"מיכה"}
* slot_getter_age{"age":"85"}
    - profile_form
    - slot{"age":"85"}
    - slot{"requested_slot":"weight"}
    - slot{"username":"מיכה"}
* slot_getter_weight{"weight":"76.5"}
    - profile_form
    - slot{"weight":"76.5"}
    - slot{"requested_slot":"height"}
* slot_getter_height{"height":"178"}
    - profile_form
    - slot{"height":"178"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username

## Name intro 6

* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username
    - utter_profile_info_getter

## Form Deny 3

* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username{"username":"ברכה"}
    - slot{"username":"ברכה"}
    - utter_profile_info_getter
* deny
    - utter_slot_getter_username_deny_details

## Form 16

* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username{"username":"קיריל"}
    - slot{"username":"קיריל"}
    - slot{"username":"קיריל"}
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
* slot_getter_age{"age":"41"}
    - profile_form
    - slot{"age":"41"}
    - slot{"requested_slot":"weight"}
    - slot{"username":"קיריל"}
* slot_getter_weight{"weight":"83"}
    - profile_form
    - slot{"weight":"83"}
    - slot{"requested_slot":"height"}
    - slot{"username":"קיריל"}
* slot_getter_height{"height":"173"}
    - profile_form
    - slot{"height":"173"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username

## Form 17

* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username{"username":"משה"}
    - slot{"username":"משה"}
    - slot{"username":"משה"}
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* slot_getter_gender{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
* slot_getter_age{"age":"23"}
    - profile_form
    - slot{"age":"23"}
    - slot{"requested_slot":"weight"}
    - slot{"username":"משה"}
* slot_getter_weight{"weight":"70"}
    - profile_form
    - slot{"weight":"70"}
    - slot{"requested_slot":"height"}
    - slot{"username":"משה"}
* slot_getter_height{"height":"180"}
    - profile_form
    - slot{"height":"180"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username

## Form 18

* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
* slot_getter_age{"age":"19"}
    - profile_form
    - slot{"age":"19"}
    - slot{"requested_slot":"weight"}
* slot_getter_weight{"weight":"67"}
    - profile_form
    - slot{"weight":"67"}
    - slot{"requested_slot":"height"}
* slot_getter_height{"height":"183"}
    - profile_form
    - slot{"height":"183"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username

## Form 19

* greet
    - utter_greet
* Bot_introduction
    - utter_my_name_is_newt
* slot_getter_username{"username":"גיל"}
    - slot{"username":"גיל"}
    - slot{"username":"גיל"}
    - utter_profile_info_getter
* affirm
    - profile_form
    - form{"name":"profile_form"}
    - slot{"requested_slot":"gender"}
* inform{"gender":"זכר"}
    - profile_form
    - slot{"gender":"זכר"}
    - slot{"requested_slot":"age"}
    - slot{"username":"גיל"}
* slot_getter_age{"age":"38"}
    - profile_form
    - slot{"age":"38"}
    - slot{"requested_slot":"weight"}
    - slot{"username":"גיל"}
* slot_getter_weight{"weight":"72"}
    - profile_form
    - slot{"weight":"72"}
    - slot{"requested_slot":"height"}
* slot_getter_height{"height":"183"}
    - profile_form
    - slot{"height":"183"}
    - form{"name":null}
    - slot{"requested_slot":null}
    - utter_slot_getter_username
