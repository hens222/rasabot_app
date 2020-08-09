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
                         index_col=["Entity Alias"],
                         usecols=["Entity Alias", "Entity", "Units", 
                                  "action_simple_question",
                                  "action_nutrition_howmanyxiny_x",
                                  "action_nutrition_howmanyxiny_y"]).fillna(0)

    # "Zameret_hebrew_features"
    url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&gid=1706335378"
    s = requests.get(url).content
    custom_df = pd.read_csv(io.StringIO(s.decode('utf-8')),
                            header=0,
                            index_col=["Entity"]).fillna(0)

    # "Zameret_hebrew_features"
    url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&gid=495295419"
    s = requests.get(url).content
    common_df = pd.read_csv(io.StringIO(s.decode('utf-8')),
                         header=0,
                         index_col=["common_name"],
                         usecols=["common_name", "shmmitzrach", "smlmitzrach"]).fillna(0)

    return db_df, lut_df, custom_df, common_df

# ------------------------------------------------------------------

class ActionSimpleQuestion(Action):

    def name(self) -> Text:
        return "action_simple_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        _, lut_df, custom_df, _ = load_db()
        
        user_intent = tracker.latest_message.get('intent').get('name')    
        
        for ent in tracker.latest_message.get('entities'):
            if ent['entity'] in lut_df[self.name()].values:
                simple_entity = ent['value']

        try:
            feature = lut_df['Entity'][simple_entity]
            
            if feature in custom_df:
                res = custom_df.loc[feature][user_intent]
            else:
                res = custom_df[[str(s) in feature for s in custom_df.index.tolist()]][user_intent][0]

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

        db_df, lut_df, _, common_df = load_db()
        
        user_msg = tracker.latest_message.get('text')    
       
        x = None
        y = None

        for ent in tracker.latest_message.get('entities'):
            if ent['entity'] in lut_df[self.name() + "_x"].values:
                x = ent['value']
            elif ent['entity'] in lut_df[self.name() + "_y"].values:
                y = ent['value']

        if not y:
            regex_res = re.search('כמה .* יש ב(.*)', user_msg)
            if regex_res:
                y = regex_res.group(1)

        try:
            y_common = y
            if y in common_df.index:
                y_common = common_df[common_df.index == y]['shmmitzrach'][0]      
            food = db_df[db_df['shmmitzrach'].str.contains(y_common)].iloc[0,:]    
            feature = lut_df[lut_df.index == x]["Entity"][0]
            units = lut_df[lut_df.index == x]["Units"][0]

            res = food[feature]

            if units == 0:
                dispatcher.utter_message(text="ב-100 גרם %s יש %.2f %s" % (food['shmmitzrach'], float(res), x))
            else:
                dispatcher.utter_message(text="ב-100 גרם %s יש %.2f %s %s" % (food['shmmitzrach'], float(res), units, x))
        
        except:
            dispatcher.utter_message(text="אין לי מושג כמה, מצטער!")

        return []

# ------------------------------------------------------------------

class ActionEatBeforeTrainingQuestion(Action):

    def name(self) -> Text:
        return "action_eat_before_training"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_intent = tracker.latest_message.get('intent').get('name')
        
        training_type = tracker.get_slot("training_type")
        training_duration = tracker.get_slot("training_duration")
        
        try:
            _, _, custom_df = load_db()
            
            if training_type == 'ריצת אינטרוולים':
                if training_duration:
                    res = custom_df['Entity'][training_type + ' מעל ' + training_duration][0]
                else:
                    res = custom_df['Entity'][training_type][0]

            dispatcher.utter_message(text="%s" % res)

        except:
            dispatcher.utter_message(text="אין לי מושג, מצטער!")

        return []

