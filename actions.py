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
                                  "action_nutrition_howmanyxiny_y",
                                  "action_nutrition_is_food_healthy",
                                  "action_nutrition_what_is_healthier_x",
                                  "action_nutrition_what_is_healthier_y"]).fillna(0)

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

    # "Newt Machine Readable"
    url = "https://docs.google.com/spreadsheets/d/1IPTflCe6shaP-FBAuXWSFCX5hSuAo7bMGczNMTSTYY0/export?format=csv&gid=885087351"
    s = requests.get(url).content
    food_ranges_df = pd.read_csv(io.StringIO(s.decode('utf-8')),
                                      header=0,
                                      index_col=["Nutrient"],
                                      usecols=["Nutrient", "Medium - threshold per 100gr", "High - threshold per 100gr",
                                               "good_or_bad", "tzameret_name", "hebrew_name"]).fillna(0)

    return db_df, lut_df, custom_df, common_df, food_ranges_df

# ------------------------------------------------------------------

class ActionSimpleQuestion(Action):

    def name(self) -> Text:
        return "action_simple_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        _, lut_df, custom_df, _, _ = load_db()
        
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

        db_df, lut_df, _, common_df, _ = load_db()
        
        user_msg = tracker.latest_message.get('text')    
       
        x = None
        y = None

        for ent in tracker.latest_message.get('entities'):
            if ent['entity'] in lut_df[self.name() + "_x"].values:
                x = ent['value']
            elif ent['entity'] in lut_df[self.name() + "_y"].values:
                y = ent['value']

        if not y:
            regex_res = re.search('כמה .* יש ב(.*)', user_msg.replace('?',''))
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
            
        _, _, custom_df, _ = load_db()

        user_intent = tracker.latest_message.get('intent').get('name')
        
        training_type = tracker.get_slot("training_type")
        training_duration = tracker.get_slot("training_duration")
        
        try:
            if training_type == 'ריצת אינטרוולים':
                if training_duration:
                    res = custom_df['Entity'][training_type + ' מעל ' + training_duration][0]
                else:
                    res = custom_df['Entity'][training_type][0]

            dispatcher.utter_message(text="%s" % res)

        except:
            dispatcher.utter_message(text="אין לי מושג, מצטער!")

        return []

# ------------------------------------------------------------------

class ActionIsFoodHealthyQuestion(Action):

    def name(self) -> Text:
        return "action_nutrition_is_food_healthy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        db_df, lut_df, _, common_df, food_ranges_df = load_db()

        for ent in tracker.latest_message.get('entities'):
            if ent['entity'] in lut_df[self.name()].values:
                food_entity = ent['value']
       
        try:
            food = food_entity
            if food in common_df.index:
                food = common_df[common_df.index == food]['shmmitzrach'][0]      
            
            food = db_df[db_df['shmmitzrach'].str.contains(food)].iloc[0,:]    
        
            nutrition_density = food_ranges_df[food_ranges_df.index == "Nutrition density"]
            nutrition_density_med = float(nutrition_density["Medium - threshold per 100gr"])
            nutrition_density_high = float(nutrition_density["High - threshold per 100gr"])
        
            advantages = []
            disadvantages = []
        
            for idx, row in food_ranges_df.iterrows():
        
                if row["good_or_bad"] == "good":
                    value = float(food[row["tzameret_name"]])
                    if idx == "Protein":
                        threshold = 250
                    else:
                        threshold = float(row["Medium - threshold per 100gr"])
                    if value > threshold:
                        advantages.append(row["hebrew_name"])
        
                elif row["good_or_bad"] == "bad":
                    value = float(food[row["tzameret_name"]])
                    if idx == "Protein":
                        threshold = 250
                    else:
                        threshold = float(row["High - threshold per 100gr"])
                    if value > threshold:
                        disadvantages.append(row["hebrew_name"])
                
            nutrition_density_normalized = float(food["Nutrition density normalized"])
            
            if nutrition_density_normalized < nutrition_density_med:
                res = "ב%s יש צפיפות תזונתית (רכיבים תזונתיים טובים ביחס לקלוריות) נמוכה" % food_entity
            elif nutrition_density_normalized < nutrition_density_high:
                res = "ב%s יש צפיפות תזונתית (רכיבים תזונתיים טובים ביחס לקלוריות) בינונית" % food_entity
            else:
                res = "ב%s יש צפיפות תזונתית (רכיבים תזונתיים טובים ביחס לקלוריות) גבוהה" % food_entity
        
            if disadvantages:
                res += ". "
                res += "החסרונות של %s הם הרבה %s" % (food_entity, ", ".join(disadvantages))
        
            if advantages:
                res += ". "
                res += "היתרונות של %s הם הרבה %s" % (food_entity, ", ".join(advantages))
            
            dispatcher.utter_message(text="%s" % res)
        
        except:
            dispatcher.utter_message(text="אין לי מושג, מצטער!")

        return []

# ------------------------------------------------------------------

class ActionWhatIsHealthierQuestion(Action):

    def name(self) -> Text:
        return "action_nutrition_what_is_healthier"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        db_df, lut_df, _, common_df, food_ranges_df = load_db()
        
        user_msg = tracker.latest_message.get('text')    
       
        food_entity1 = None
        food_entity2 = None

        for ent in tracker.latest_message.get('entities'):
            if ent['entity'] in lut_df[self.name() + "_x"].values:
                food_entity1 = ent['value']
            elif ent['entity'] in lut_df[self.name() + "_y"].values:
                food_entity2 = ent['value']

        if not food_entity2:
            regex_res = re.search('.* או (.*)', user_msg.replace('?',''))
            if regex_res:
                food_entity2 = regex_res.group(1)

        try:
        
            nutrition_density_cmp = []
            advantages_cmp = []
            disadvantages_cmp = []
        
            for food_entity in (food_entity1, food_entity2):
        
                food = food_entity
        
                if food in common_df.index:
                    food = common_df[common_df.index == food]['shmmitzrach'][0]      
                
                food = db_df[db_df['shmmitzrach'].str.contains(food)].iloc[0,:]    
        
                nutrition_density = food_ranges_df[food_ranges_df.index == "Nutrition density"]
                nutrition_density_med = float(nutrition_density["Medium - threshold per 100gr"])
                nutrition_density_high = float(nutrition_density["High - threshold per 100gr"])
        
                advantages = []
                disadvantages = []
        
                for idx, row in food_ranges_df.iterrows():
        
                    if row["good_or_bad"] == "good":
                        value = float(food[row["tzameret_name"]])
                        if idx == "Protein":
                            threshold = 250
                        else:
                            threshold = float(row["Medium - threshold per 100gr"])
                        if value > threshold:
                            advantages.append(row["hebrew_name"])
        
                    elif row["good_or_bad"] == "bad":
                        value = float(food[row["tzameret_name"]])
                        if idx == "Protein":
                            threshold = 250
                        else:
                            threshold = float(row["High - threshold per 100gr"])
                        if value > threshold:
                            disadvantages.append(row["hebrew_name"])                
              
                nutrition_density_cmp.append(float(food["Nutrition density normalized"]))
        
                if disadvantages:
                    disadvantages_cmp.append("החסרונות של %s הם הרבה %s" % (food_entity, ", ".join(disadvantages)))
        
                if advantages:
                    advantages_cmp.append("היתרונות של %s הם הרבה %s" % (food_entity, ", ".join(advantages)))
        
            if nutrition_density_cmp[0] > nutrition_density_cmp[1]:
                res = "לפי צפיפות תזונתית %s עדיף על פני %s\n" % (food_entity1, food_entity2)
            elif nutrition_density_cmp[0] < nutrition_density_cmp[1]:
                res = "לפי צפיפות תזונתית %s עדיף על פני %s\n" % (food_entity2, food_entity1)
            else:
                res = "לפי צפיפות תזונתית %s ו-%s שקולים\n" % (food_entity1, food_entity2)
        
            for advantage in advantages_cmp:
                if advantage:
                    res += "%s\n" % advantage
        
            for disadvantage in disadvantages_cmp:
                if disadvantage:
                    res += "%s\n" % disadvantage
            
            dispatcher.utter_message(text="%s" % res)
        
        except:
            dispatcher.utter_message(text="אין לי מושג כמה, מצטער!")
        
        return []

