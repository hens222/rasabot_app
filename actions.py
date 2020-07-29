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

def load_db():

    # "Zameret food list 22_JAN_2020"
    url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&gid=84892416"
    s = requests.get(url).content
    db_df = pd.read_csv(io.StringIO(s.decode('utf-8'))).fillna(0)

    # "Zameret_hebrew_features"
    url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&gid=1805881936"
    s = requests.get(url).content
    lut_df = pd.read_csv(io.StringIO(s.decode('utf-8')),
                         header=0,
                         index_col=["Feature Alias"],
                         usecols=["Feature Alias", "Zameret Feature", "Units"]).fillna(0)

    # "Zameret_hebrew_features"
    url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&gid=1805881936"
    s = requests.get(url).content
    custom_df = pd.read_csv(io.StringIO(s.decode('utf-8')),
                            header=0,
                            index_col=["Zameret Nutrient"],
                            usecols=["Zameret Nutrient", "Definition", "Importance", "WhatHas"]).fillna(0)

    return db_df, lut_df, custom_df

# ------------------------------------------------------------------

class ActionSimpleQuestion(Action):

    def name(self) -> Text:
        return "action_simple_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_msg = tracker.latest_message.get('text')
        user_intent = tracker.latest_message.get('intent').get('name')
        #user_entities = tracker.latest_message.get('entities')

        x = user_msg.split(' ')[-1]

        action_col = "NA"
        if user_intent == "nutrition_definition":
            action_col = "Definition"
        elif user_intent == "nutrition_what_has":
            action_col = "WhatHas"
        elif user_intent == "nutrition_importance":
            action_col = "Importance"

        try:
            db_df, lut_df, custom_df = load_db()

            feature = lut_df[[x in s for s in lut_df.index.tolist()]]["Zameret Feature"][0]
            res = custom_df[[str(s) in feature for s in custom_df.index.tolist()]][action_col][0]

            dispatcher.utter_message(text="%s" % res)

        except:
            dispatcher.utter_message(text="אין לי מושג, מצטער!")

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

            db_df, lut_df, _ = load_db()

            try:
                food = db_df[db_df['shmmitzrach'].str.contains(y)].iloc[0,:]
                feature = lut_df[lut_df.index == x]["Zameret Feature"][0]
                units = lut_df[lut_df.index == x]["Units"][0]

                res = food[feature]

                if units == 0:
                    dispatcher.utter_message(text="ב-100 גרם %s יש %.2f %s" % (food['shmmitzrach'], float(res), x))
                else:
                    dispatcher.utter_message(text="ב-100 גרם %s יש %.2f %s %s" % (food['shmmitzrach'], float(res), units, x))
            except:
                dispatcher.utter_message(text="אין לי מושג כמה %s יש ב-%s, מצטער!" % (x,y))

        else:
            dispatcher.utter_message(text="אין לי מושג כמה, מצטער!")

        return []

