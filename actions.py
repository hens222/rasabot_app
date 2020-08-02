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
                         usecols=["Entity Alias", "Entity", "Units"]).fillna(0)

    # "Zameret_hebrew_features"
    url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&gid=1706335378"
    s = requests.get(url).content
    custom_df = pd.read_csv(io.StringIO(s.decode('utf-8')),
                            header=0,
                            index_col=["Entity"]).fillna(0)

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

        def find_feature(lut_df, user_msg):
            entity = 'N/A'
            entity_buckets = {'Priority1': [], 
                              'Priority2': [],
                              'Priority3': []}
            q = user_msg.replace('?','').split(' ')
          
            for k,entity_alias in enumerate(lut_df.index.tolist()):
                if ' '.join(q[-2:]) in entity_alias:
                    entity_buckets['Priority1'].append(lut_df['Entity'][k])
                elif q[-1] in entity_alias:
                    entity_buckets['Priority2'].append(lut_df['Entity'][k])
                elif q[-2] in entity_alias:
                    entity_buckets['Priority3'].append(lut_df['Entity'][k])
          
            if entity_buckets['Priority1']:
                entity = entity_buckets['Priority1'][0]
            elif entity_buckets['Priority2']:
                entity = entity_buckets['Priority2'][0] 
            elif entity_buckets['Priority3']:
                entity = entity_buckets['Priority3'][0]
          
            return entity
        
        try:
            db_df, lut_df, custom_df = load_db()

            feature = find_feature(lut_df, user_msg)
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

        user_msg = tracker.latest_message.get('text')

        regex_res = re.search('כמה (.*) יש ב(.*)', user_msg)

        if regex_res:

            x = regex_res.group(1)
            y = regex_res.group(2)

            db_df, lut_df, _ = load_db()

            try:
                food = db_df[db_df['shmmitzrach'].str.contains(y)].iloc[0,:]
                feature = lut_df[lut_df.index == x]["Entity"][0]
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

