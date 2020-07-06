# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionNutritionDefinition(Action):

    def name(self) -> Text:
        return "action_nutrition_definition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_msg = tracker.latest_message.get('text')

        if "פחממות"  in user_msg or \
           "פחמימות" in user_msg:
            dispatcher.utter_message(text="פחממה היא הדבר הבא!")
        
        elif "חלבון" in user_msg:
            dispatcher.utter_message(text="חלבון זה הלבן בביצה")

        else:
            dispatcher.utter_message(text="מצטער, לא הבנתי את השאלה")

        return []

# ------------------------------------------------------------------

class ActionNutritionWhatHas(Action):

    def name(self) -> Text:
        return "action_nutrition_what_has"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_msg = tracker.latest_message.get('text')

        if "פחממות"  in user_msg or \
           "פחמימות" in user_msg:
            dispatcher.utter_message(text="פחממות יש בלחם למשל")
        
        elif "חלבון" in user_msg:
            dispatcher.utter_message(text="חלבון יש במוצרי חלב")

        else:
            dispatcher.utter_message(text="מצטער, לא הבנתי את השאלה")

        return []

# ------------------------------------------------------------------

class ActionNutritionImportance(Action):

    def name(self) -> Text:
        return "action_nutrition_importance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_msg = tracker.latest_message.get('text')

        if "פחממות"  in user_msg or \
           "פחמימות" in user_msg:
            dispatcher.utter_message(text="פחממות הן מקור האנרגיה שלנו")
        
        elif "חלבון" in user_msg:
            dispatcher.utter_message(text="חלבון מחזק את העצמות שלנו")

        else:
            dispatcher.utter_message(text="זה דבר ממש בריא!")

        return []

