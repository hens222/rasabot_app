# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

import re
import io
import requests
import pandas as pd
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

# ------------------------------------------------------------------

class ActionNutritionHowManyXinY(Action):

    def name(self) -> Text:
        return "action_nutrition_howmanyxiny"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_msg = tracker.latest_message.get('text')

        regex_res = re.search('כמה (.*) יש ב(.*)', user_msg)

        if regex_res:
            x = regex_res.group(1)
            y = regex_res.group(2)

        sheet = "Zameret food list 22_JAN_2020"
        url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&sheet=%s" % sheet
        s = requests.get(url).content
        df = pd.read_csv(io.StringIO(s.decode('utf-8')))

        try:
            dispatcher.utter_message(text="ב%s יש %f %s" % (y, float(df[df['shmmitzrach']==y][x]), x))
        except:
            dispatcher.utter_message(text="אין לי מושג כמה %s יש ב-%s, מצטער!" % (x,y))

        return []

