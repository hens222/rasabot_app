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
from os import path
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

def load_db(db_bitmap):

    db_dict = {}
  
    # "Zameret food list 22_JAN_2020"
    if (db_bitmap & 0x1) > 0:
        url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&gid=84892416"
        s = requests.get(url).content
        db_dict['tzameret'] = pd.read_csv(io.StringIO(s.decode('utf-8'))).fillna(0)
  
    # "Zameret_hebrew_features" - entities aliases
    if (db_bitmap & 0x2) > 0:    
        url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&gid=1805881936"
        s = requests.get(url).content
        db_dict['lut'] = pd.read_csv(io.StringIO(s.decode('utf-8')),
                                     header=0,
                                     index_col=["Entity Alias"],
                                     usecols=["Entity Alias", "Entity", "Units", 
                                              "Entity name", "RDA name",
                                              "action_simple_question",
                                              "action_nutrition_howmanyxiny_x",
                                              "action_nutrition_howmanyxiny_y",
                                              "action_nutrition_is_food_healthy",
                                              "action_nutrition_is_food_recommended",
                                              "action_nutrition_what_is_healthier_x",
                                              "action_nutrition_what_is_healthier_y",
                                              "action_nutrition_get_rda",
                                              "action_nutrition_bloodtest_generic",
                                              "action_nutrition_bloodtest_value"]).fillna(0)
  
    # "Zameret_hebrew_features" - nutrients_questions
    if (db_bitmap & 0x4) > 0:    
        url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&gid=1706335378"
        s = requests.get(url).content
        db_dict['nutrients_qna'] = pd.read_csv(io.StringIO(s.decode('utf-8')),
                                               header=0,
                                               index_col=["Entity"]).fillna(0)
  
    # "Zameret_hebrew_features" - Food questions
    if (db_bitmap & 0x8) > 0:    
        url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&gid=1099284657"
        s = requests.get(url).content
        db_dict['food_qna'] = pd.read_csv(io.StringIO(s.decode('utf-8')),
                                          header=0,
                                          index_col=["nutrition_density"],
                                          usecols=["nutrition_density", "energy_density", "description_density"]).fillna(0)
  
    # "Zameret_hebrew_features" - List of common foods
    if (db_bitmap & 0x10) > 0:
        url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&gid=495295419"
        s = requests.get(url).content
        db_dict['common_food'] = pd.read_csv(io.StringIO(s.decode('utf-8')),
                                             header=0,
                                             index_col=["common_name"],
                                             usecols=["common_name", "shmmitzrach", "smlmitzrach"]).fillna(0)
  
    # "Newt Machine Readable" - FoodItemRanges
    if (db_bitmap & 0x20) > 0:    
        url = "https://docs.google.com/spreadsheets/d/1IPTflCe6shaP-FBAuXWSFCX5hSuAo7bMGczNMTSTYY0/export?format=csv&gid=885087351"
        s = requests.get(url).content
        db_dict['food_ranges'] = pd.read_csv(io.StringIO(s.decode('utf-8')),
                                             header=0,
                                             index_col=["Nutrient"],
                                             usecols=["Nutrient", "Medium - threshold per 100gr", "High - threshold per 100gr",
                                                      "good_or_bad", "tzameret_name", "hebrew_name"]).fillna(0)
  
    # "Newt Machine Readable" - MicroNutrients
    if (db_bitmap & 0x40) > 0:    
        url = "https://docs.google.com/spreadsheets/d/1IPTflCe6shaP-FBAuXWSFCX5hSuAo7bMGczNMTSTYY0/export?format=csv&gid=222801095"
        s = requests.get(url).content
        micro_nutrients_df = pd.read_csv(io.StringIO(s.decode('utf-8')),
                                         header=0).fillna(0)
        db_dict['micro_nutrients'] = micro_nutrients_df[micro_nutrients_df['Type'] == "RDA"]
 
    # "Newt Machine Readable" - MicroNutrients
    if (db_bitmap & 0x80) > 0:
        url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&gid=1373096469"
        s = requests.get(url).content
        food_units_df = pd.read_csv(io.StringIO(s.decode('utf-8')),
                                    header=0).fillna(0)
        db_dict['food_units'] = food_units_df

    # "Newt Machine Readable" - BloodTestValues
    if (db_bitmap & 0x100) > 0:
        url = "https://docs.google.com/spreadsheets/d/1IPTflCe6shaP-FBAuXWSFCX5hSuAo7bMGczNMTSTYY0/export?format=csv&gid=1011022304"
        s = requests.get(url).content
        bloodtest_df = pd.read_csv(io.StringIO(s.decode('utf-8')),
                                   header=0, nrows=19, usecols=range(11)).fillna(0)
        db_dict['bloodtest_vals'] = bloodtest_df

    # "Zameret_hebrew_features" - Weight aliases
    if (db_bitmap & 0x200) > 0:
        url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&gid=623521836"
        s = requests.get(url).content
        food_units_aliases_df = pd.read_csv(io.StringIO(s.decode('utf-8')), header=0)
        db_dict['food_units_aliases'] = food_units_aliases_df

    return db_dict

# ------------------------------------------------------------------

def get_rda(name, tracker, nutrient=None):

    db_dict = load_db(0x46) 
    
    lut_df = db_dict['lut']
    custom_df = db_dict['nutrients_qna']
    micro_nutrients_df = db_dict['micro_nutrients']
    
    status = "match"
    if not (tracker.get_slot('gender') and tracker.get_slot('age') and tracker.get_slot('weight') and tracker.get_slot('height')):
        status = "default"
   
    for ent in tracker.latest_message.get('entities'):
        if ent['entity'] in lut_df[name].values:
            nutrient = ent['value']
            break

    try:

        feature = lut_df['Entity'][nutrient]
        feature_rda = lut_df['RDA name'][lut_df['Entity name'] == feature][0]
        
        gender = "Male"
        if tracker.get_slot('gender') == "זכר":
            gender = "Male"
        elif tracker.get_slot('gender') == "נקבה":
            gender = "Female" 

        user_vars = {}

        user_vars['age'] = tracker.get_slot('age') if tracker.get_slot('age') else "40"
        user_vars['weight'] = tracker.get_slot('weight') if tracker.get_slot('weight') else "80"
        user_vars['height'] = tracker.get_slot('height') if tracker.get_slot('height') else "180"
            
        rda_row = micro_nutrients_df[(micro_nutrients_df['Micronutrient'] == feature_rda) & \
                                     ((micro_nutrients_df['Gender'] == "ANY")    | (micro_nutrients_df['Gender'] == gender)) & \
                                     ((micro_nutrients_df['Pregnancy'] == "ANY") | (micro_nutrients_df['Pregnancy'] == "No")) & \
                                     ((micro_nutrients_df['Lactating'] == "ANY") | (micro_nutrients_df['Lactating'] == "No")) & \
                                     ((micro_nutrients_df['Age Min'] == "ANY")   | (micro_nutrients_df['Age Min'].astype(float) <= int(user_vars['age']))) & \
                                     ((micro_nutrients_df['Age Max'] == "ANY")   | (micro_nutrients_df['Age Max'].astype(float) > int(user_vars['age'])))]
    
        rda_text = rda_row['Free Text'].values[0]
        rda_value = rda_row['Value'].values[0]
        rda_units = rda_row['Units'].values[0]

        if 'slot#' in rda_value:
            rda_value_list = rda_value.split(' ')
            for k,el in enumerate(rda_value_list):
                if 'slot#' in el and el.split('#')[1] in user_vars:
                    rda_value_list[k] = user_vars[el.split('#')[1]]
            rda_value = eval(' '.join(rda_value_list))    

        rda_value = float(rda_value)

        return rda_value, rda_text, rda_units, status, nutrient

    except:

        return -1, -1, "", "missmatch", nutrient

# ------------------------------------------------------------------

def get_personal_str(rda_status, tracker): 

    age = tracker.get_slot('age') if tracker.get_slot('age') and rda_status == "match" else '40'
    gender = tracker.get_slot('gender') if tracker.get_slot('gender') and rda_status == "match" else 'זכר'
    weight = tracker.get_slot('weight') if tracker.get_slot('weight') and rda_status == "match" else '80'
    height = tracker.get_slot('height') if tracker.get_slot('height') and rda_status == "match" else '180'

    if rda_status == "default":
        personal_str = "עבור %s בגיל %s במשקל %s ובגובה %s" % (gender, age, weight, height)
    else:
        personal_str = "עבורך (%s בגיל %s במשקל %s ובגובה %s)" % (gender, age, weight, height)    

    return personal_str

# ------------------------------------------------------------------

def get_food_nutrition_density(food, food_ranges_db):

    # Nutrition Density is defined in Tzameret:
    density_normalized = float(food["Nutrition density normalized"])
  
    # Thresholds are defined in Machine-Readable:
    density = food_ranges_db[food_ranges_db.index == "Nutrition density"]
    density_med = float(density["Medium - threshold per 100gr"])
    density_high = float(density["High - threshold per 100gr"])
  
    # Binning:
    res = "high"
    if density_normalized < density_med:
        res = "low"
    elif density_normalized < density_high:
        res = "med"
  
    return density, res

# ------------------------------------------------------------------

def get_food_energy_density(food, food_ranges_db):

    # Energy Density is defined in Tzameret:
    density_normalized = float(food["Energy density"])
  
    # Thresholds are defined in Machine-Readable:
    density = food_ranges_db[food_ranges_db.index == "Energy density"]
    density_med = float(density["Medium - threshold per 100gr"])
    density_high = float(density["High - threshold per 100gr"])
  
    # Binning:
    res = "high"
    if density_normalized < density_med:
        res = "low"
    elif density_normalized < density_high:
        res = "med"
  
    return density, res

# ------------------------------------------------------------------

class ActionSimpleQuestion(Action):

    def name(self) -> Text:
        return "action_simple_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        db_dict = load_db(0x6)
        
        lut_df = db_dict['lut']
        custom_df = db_dict['nutrients_qna']
        
        user_intent = tracker.latest_message.get('intent').get('name')    
         
        for ent in tracker.latest_message.get('entities'):
            if ent['entity'] in lut_df[self.name()].values:
                simple_entity = ent['value']
                break

        try:
            feature = lut_df['Entity'][simple_entity]
            
            if feature in custom_df:
                res = custom_df.loc[feature][user_intent]
            else:
                res = custom_df[[str(s) in feature for s in custom_df.index.tolist()]][user_intent][0]

            res_list = res.split(' ')
            for i,el in enumerate(res_list):
                if "#" in el:
                    k,v = el.split('#')
                    if k == "slot":
                        if v.endswith(','):
                            token = tracker.get_slot(v.replace(',','')) + ','
                        else:
                            token = tracker.get_slot(v.replace(',',''))
                        if token:
                            res_list[i] = token
                        else:
                            res_list[i] = "_"
                    elif k == "equation":
                        try:
                            res_list[i] = str(eval(v))
                        except:
                            res_list[i] = "_"

            res = ' '.join(res_list)
            
            dispatcher.utter_message(text="%s" % res)

        except:
            dispatcher.utter_message(text="אין לי מושג, מצטער!")

        return []

# ------------------------------------------------------------------

class ActionGetRDAQuestion(Action):

    def name(self) -> Text:
        return "action_nutrition_get_rda"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        rda_val, rda_units, rda_text, rda_status, nutrient = get_rda(self.name(), tracker)

        if rda_val > 0:

            res = "הקצובה היומית המומלצת של %s %s היא\n %.2f %s" % \
                  (nutrient, get_personal_str(rda_status, tracker), rda_val, rda_units)
            
            if rda_text:
                res += '\n' + rda_text
        
        else:

            res = "אין לי מושג, מצטער!"
            
        dispatcher.utter_message(text="%s" % res)

        return []

# ------------------------------------------------------------------

class ActionNutritionHowManyXinY(Action):

    def name(self) -> Text:
        return "action_nutrition_howmanyxiny"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        db_dict = load_db(0x293)
       
        db_df = db_dict['tzameret']
        lut_df = db_dict['lut']
        common_df = db_dict['common_food']
        units_df = db_dict['food_units']
        units_aliases_df = db_dict['food_units_aliases']
      
        user_msg = tracker.latest_message.get('text')    
      
        # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        # Fetch X and Y (from slots, from entities or from regex):
      
        y = None
        x = tracker.get_slot('x') if tracker.get_slot('x') else None
        if tracker.latest_message.get('entities'):
            y = tracker.get_slot('y') if tracker.get_slot('y') else None

        name_xy = self.name() + "_x"
        for ent in tracker.latest_message.get('entities'):
            if ent['entity'] in lut_df[self.name() + "_x"].values:
                x = ent['value']
                name_xy = self.name() + "_x"
            elif ent['entity'] in lut_df[self.name() + "_y"].values:
                y = ent['value']
                name_xy = self.name() + "_y"

        regex_res = re.search('כמה (.*) יש ב(.*)', user_msg.replace('?',''))
        if regex_res:
            x = regex_res.group(1)
            y = regex_res.group(2)
        
        if not y:
            regex_res = re.search('.* ב(.*)', user_msg.replace('?',''))
            if regex_res:
                y = regex_res.group(1)
       
        food_units = "100 גרם"
        regex_units_res = re.search('(.*) של (.*)', y)
        if regex_units_res:
            food_units = regex_units_res.group(1)
            y = regex_units_res.group(2)

        if food_units in units_aliases_df['Unit Alias'].values:
            food_units = units_aliases_df[units_aliases_df['Unit Alias'] == food_units]['Zameret unit'].values[0]

        # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        
        try:
            y_common = y
            if y in common_df.index:
                y_common = common_df[common_df.index == y]['shmmitzrach'][0]
            else:
                y_food = ' '.join(y.split(' ')[1:])
                food_units = units_aliases_df[units_aliases_df['Unit Alias'] == y.split(' ')[0]]['Zameret unit']
                if food_units.empty:
                    food_units = y.split(' ')[0]
                else:
                    food_units = food_units.values[0]
                if y_food in common_df.index:
                    y_common = common_df[common_df.index == y_food]['shmmitzrach'][0]            
                else:
                    y_common = y_food

            food = db_df[db_df['shmmitzrach'].str.contains(y_common)].iloc[0,:]    
            feature = lut_df[lut_df.index == x]["Entity"][0]
            units = lut_df[lut_df.index == x]["Units"][0]

            food_units_row = pd.Series()
            if food_units:
                food_units_row = units_df[(units_df['smlmitzrach'] == int(food['smlmitzrach'])) &
                                          (units_df['shmmida'] == food_units)]

            is_food_units_match = not food_units_row.empty or food_units == "100 גרם"

            food_units_factor = 1.0
            if not food_units_row.empty:
                food_units_factor = food_units_row['mishkal'].values[0]/100

            val = food[feature] * food_units_factor


            if units == 0:
                res = "ב-%s של %s יש %.2f %s" % (food_units, food['shmmitzrach'], float(val), x)
            else:
                res = ""        
                if not is_food_units_match:            
                    res = "לא הצלחתי למצוא נתונים במאגר על היחידה %s עליה שאלת\n" % food_units
                    res += "היחידות הבאות קיימות במאגר, עבור %s:\n" % food['shmmitzrach']
                    res += ', '.join(units_df[units_df['smlmitzrach'] == int(food['smlmitzrach'])]['shmmida'].to_list())
                    res += "\n"
                    food_units = "100 גרם"
                
                res += "ב-%s של %s יש %.2f %s %s" % (food_units, food['shmmitzrach'], float(val), units, x)

            rda_val, rda_units, rda_text, rda_status, nutrient = get_rda(name_xy, tracker)

            if rda_val > 0 and units not in ['יחב"ל']:
                rda = 100 * float(val) / rda_val
                res += "\n"
                res += "שהם כ-%d אחוז מהקצובה היומית המומלצת %s" % (int(rda), get_personal_str(rda_status, tracker))
            
            if rda_text:
                res += '\n' + rda_text

            dispatcher.utter_message(text="%s" % res)
        
        except:
            dispatcher.utter_message(text="אין לי מושג כמה, מצטער!")

        return [SlotSet("x", x), SlotSet("y", y)]

# ------------------------------------------------------------------

class ActionIsFoodHealthyQuestion(Action):

    def name(self) -> Text:
        return "action_nutrition_is_food_healthy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        db_dict = load_db(0x33)
       
        db_df = db_dict['tzameret']
        lut_df = db_dict['lut']
        common_df = db_dict['common_food']
        food_ranges_df = db_dict['food_ranges']

        for ent in tracker.latest_message.get('entities'):
            if ent['entity'] in lut_df[self.name()].values:
                food_entity = ent['value']
                break
       
        try:
            food = food_entity
            if food in common_df.index:
                food = common_df[common_df.index == food]['shmmitzrach'][0]      
            
            food = db_df[db_df['shmmitzrach'].str.contains(food)].iloc[0,:]    
        
            _, nutrition_density_res = get_food_nutrition_density(food, food_ranges_df)

            advantages = []
            disadvantages = []
        
            for idx, row in food_ranges_df.iterrows():
                    
                if row["tzameret_name"]:
        
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
            
            if nutrition_density_res == "low":
                res = "ב%s יש צפיפות תזונתית (רכיבים תזונתיים טובים ביחס לקלוריות) נמוכה" % food_entity
            elif nutrition_density_res == "med":
                res = "ב%s יש צפיפות תזונתית (רכיבים תזונתיים טובים ביחס לקלוריות) בינונית" % food_entity
            elif nutrition_density_res == "high":
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
        
        db_dict = load_db(0x33)
       
        db_df = db_dict['tzameret']
        lut_df = db_dict['lut']
        common_df = db_dict['common_food']
        food_ranges_df = db_dict['food_ranges']
        
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

                nutrition_density, _ = get_food_nutrition_density(food, food_ranges_df)
        
                advantages = []
                disadvantages = []
        
                for idx, row in food_ranges_df.iterrows():
                    
                    if row["tzameret_name"]:

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
       
            if nutrition_density_cmp[0] < nutrition_density_cmp[1]:
                advantages_cmp.reverse()
                disadvantages_cmp.reverse()

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

# ------------------------------------------------------------------

class ActionWhatIsRecommendedQuestion(Action):

    def name(self) -> Text:
        return "action_nutrition_is_food_recommended"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        db_dict = load_db(0x3b)
       
        db_df = db_dict['tzameret']
        lut_df = db_dict['lut']
        food_qna_df = db_dict['food_qna']
        common_df = db_dict['common_food']
        food_ranges_df = db_dict['food_ranges']
       
        for ent in tracker.latest_message.get('entities'):
            if ent['entity'] in lut_df[self.name()].values:
                food_entity = ent['value']
                break
        
        try:
            food = food_entity
            if food in common_df.index:
                food = common_df[common_df.index == food]['shmmitzrach'][0]      
            
            food = db_df[db_df['shmmitzrach'].str.contains(food)].iloc[0,:]
        
            _, nutrition_density_res = get_food_nutrition_density(food, food_ranges_df)
            _, nutrition_energy_res = get_food_energy_density(food, food_ranges_df)
        
            description_density_row = food_qna_df[(food_qna_df.index == nutrition_density_res) & 
                                                  (food_qna_df.energy_density == nutrition_energy_res)]
            res = description_density_row['description_density'].values[0]
            res = res.replace('var#food', food_entity)
            
            dispatcher.utter_message(text="%s" % res)
        
        except:
            dispatcher.utter_message(text="אין לי מושג, מצטער!")

        return []

# ------------------------------------------------------------------

class ActionEatBeforeTrainingQuestion(Action):

    def name(self) -> Text:
        return "action_eat_before_training"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        db_dict = load_db(0x10)
       
        custom_df = db_dict['common_food']

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

class ActionBloodtestGenericQuestion(Action):

    def name(self) -> Text:
        return "action_nutrition_bloodtest_generic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        db_dict = load_db(0x102)
        
        lut_df = db_dict['lut']
        bloodtest_df = db_dict['bloodtest_vals']
        
        for ent in tracker.latest_message.get('entities'):
            if ent['entity'] in lut_df[self.name()].values:
                bloodtest_entity = ent['value']
                break

        try:
            feature = db_dict['lut']['Entity'][bloodtest_entity]   

            gender_str = "Male"
            if tracker.get_slot('gender') == "זכר":
                gender_str = "Male"
            elif tracker.get_slot('gender') == "נקבה":
                gender_str = "Female" 

            age = float(tracker.get_slot('age') if tracker.get_slot('age') else "40")

            bloodtest_row = bloodtest_df[(bloodtest_df['Element'] == feature) & \
                                        ((bloodtest_df['Gender'] == "ANY") | (bloodtest_df['Gender'] == gender_str)) & \
                                        ((bloodtest_df['Age min'] == "ANY") | (bloodtest_df['Age min'].replace('ANY',-1).astype(float) <= age)) & \
                                        ((bloodtest_df['Age Max'] == "ANY") | (bloodtest_df['Age Max'].replace('ANY',-1).astype(float) > age))]

            bloodtest_type = bloodtest_row['Graph type'].values[0]
            bloodtest_min = bloodtest_row['Min'].values[0]
            bloodtest_thr1 = bloodtest_row['Threshold 1'].values[0]
            bloodtest_thr2 = bloodtest_row['Threshold 2'].values[0]
            bloodtest_max = bloodtest_row['Max'].values[0]

            if bloodtest_type == 1:
                res = 'ערך תקין עבור בדיקת %s בין %.2f ועד %.2f, ערך מעל %.2f נחשב חריג' % (bloodtest_entity, bloodtest_min, bloodtest_thr1, bloodtest_thr2)

            elif bloodtest_type == 2:
                res = 'ערך תקין עבור בדיקת %s בין %.2f ועד %.2f, ערך מתחת %.2f נחשב חריג' % (bloodtest_entity, bloodtest_thr2, bloodtest_max, bloodtest_thr1)

            elif bloodtest_type == 3:
                res = 'ערך תקין עבור בדיקת %s בין %.2f ועד %.2f' % (bloodtest_entity, bloodtest_thr1, bloodtest_thr2)

            dispatcher.utter_message(text="%s" % res)

        except:
            dispatcher.utter_message(text="אין לי מושג, מצטער!")

        return []

# ------------------------------------------------------------------

class ActionBloodtestValueQuestion(Action):

    def name(self) -> Text:
        return "action_nutrition_bloodtest_value"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        db_dict = load_db(0x102)
        
        lut_df = db_dict['lut']
        bloodtest_df = db_dict['bloodtest_vals']
        
        user_msg = tracker.latest_message.get('text')    
  
        for ent in tracker.latest_message.get('entities'):
            if ent['entity'] in [x for x in lut_df[self.name()].values if x != 0]:
                if ent['entity'] == 'integer':
                    val = ent['value']
                else:
                    bloodtest_entity = ent['value']
        
        if not val:
            regex_res = re.search('האם (.*) הוא .*', user_msg.replace('?',''))
            if regex_res:
                val = regex_res.group(1)

        try:
            if not val:
                raise Exception() 

            feature = db_dict['lut']['Entity'][bloodtest_entity]   

            gender_str = "Male"
            if tracker.get_slot('gender') == "זכר":
                gender_str = "Male"
            elif tracker.get_slot('gender') == "נקבה":
                gender_str = "Female" 

            age = float(tracker.get_slot('age') if tracker.get_slot('age') else "40")

            bloodtest_row = bloodtest_df[(bloodtest_df['Element'] == feature) & \
                                        ((bloodtest_df['Gender'] == "ANY") | (bloodtest_df['Gender'] == gender_str)) & \
                                        ((bloodtest_df['Age min'] == "ANY") | (bloodtest_df['Age min'].replace('ANY',-1).astype(float) <= age)) & \
                                        ((bloodtest_df['Age Max'] == "ANY") | (bloodtest_df['Age Max'].replace('ANY',-1).astype(float) > age))]

            bloodtest_type = bloodtest_row['Graph type'].values[0]
            bloodtest_min = bloodtest_row['Min'].values[0]
            bloodtest_thr1 = bloodtest_row['Threshold 1'].values[0]
            bloodtest_thr2 = bloodtest_row['Threshold 2'].values[0]
            bloodtest_max = bloodtest_row['Max'].values[0]

            if bloodtest_type == 1:
                if bloodtest_min <= float(val) <= bloodtest_thr1:
                    res = 'כן, זהו ערך תקין עבור בדיקת %s היות והוא נופל בטווח בין %.2f ועד %.2f. ערך מעל %.2f נחשב לחריג' % (bloodtest_entity, bloodtest_min, bloodtest_thr1, bloodtest_thr2)
                else:
                    res = 'לא, זהו אינו ערך תקין עבור בדיקת %s. ערך תקין הינו בטווח בין %.2f ועד %.2f. ערך מעל %.2f נחשב לחריג' % (bloodtest_entity, bloodtest_min, bloodtest_thr1, bloodtest_thr2)

            elif bloodtest_type == 2:
                if bloodtest_thr2 <= float(val) <= bloodtest_max:
                    res = 'כן, זהו ערך תקין עבור בדיקת %s היות והוא נופל בטווח בין %.2f ועד %.2f. ערך מתחת %.2f נחשב לחריג' % (bloodtest_entity, bloodtest_thr2, bloodtest_max, bloodtest_thr1)
                else:
                    res = 'לא, זהו אינו ערך תקין עבור בדיקת %s. ערך תקין הינו בטווח בין %.2f ועד %.2f. ערך מתחת %.2f נחשב לחריג' % (bloodtest_entity, bloodtest_thr2, bloodtest_max, bloodtest_thr1)

            elif bloodtest_type == 3:
                if bloodtest_thr1 <= float(val) <= bloodtest_thr2:
                    res = 'כן, זהו ערך תקין עבור בדיקת %s היות והוא נופל בטווח בין %.2f ועד %.2f' % (bloodtest_entity, bloodtest_thr1, bloodtest_thr2)
                else:
                    res = 'לא, זהו אינו ערך תקין עבור בדיקת %s. ערך תקין הינו בטווח בין %.2f ועד %.2f.' % (bloodtest_entity, bloodtest_thr1, bloodtest_thr2)

            else:
                raise Exception()

            dispatcher.utter_message(text="%s" % res)

        except:
            dispatcher.utter_message(text="אין לי מושג, מצטער!")

        return []

# ------------------------------------------------------------------

class ActionPersonalizationList(Action):

    def name(self) -> Text:
        return "action_personlization_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            pkl_db = './persons.pkl'
            if path.exists(pkl_db):
                df = pd.read_pickle(pkl_db)
                dispatcher.utter_message(text="%s" % df.to_string())
        except:
            dispatcher.utter_message(text="אין לי מושג, מצטער!")

        return []

# ------------------------------------------------------------------

class ActionPersonalizationRemove(Action):

    def name(self) -> Text:
        return "action_personlization_remove"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            pkl_db = './persons.pkl'
            if path.exists(pkl_db):
                df = pd.read_pickle(pkl_db)
                phone_slot = tracker.get_slot("phone")
                if phone_slot in df.index:
                    df = df.drop(tracker.get_slot("phone"))
                    df.to_pickle(pkl_db)
                    dispatcher.utter_message(text="רישומך הוסר מן המערכת")
                else:
                    dispatcher.utter_message(text="אינך מופיע במערכת, לכן אין צורך בהסרת רישום")
        except:
            dispatcher.utter_message(text="אין לי מושג, מצטער!")

        return []

# ------------------------------------------------------------------

class ProfileForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "profile_form"

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["phone", "username", "gender", "age", "weight", "height"]

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "phone": [
                self.from_entity(entity="integer", role="phone"),
                self.from_entity(entity="integer"),
                self.from_text(),
            ],
            "username": [
                self.from_entity(entity="name"),
                self.from_text(),
            ],
            "gender": [
                self.from_entity(entity="gender"),
            ],
            "age": [
                self.from_entity(entity="integer", role="age"),
                self.from_entity(entity="integer"),
                self.from_text(),
            ],
            "weight": [
                self.from_entity(entity="integer", role="weight"),
                self.from_entity(entity="integer"),
                self.from_text(),
            ],
            "height": [
                self.from_entity(entity="integer", role="height"),
                self.from_entity(entity="integer"),
                self.from_text(),
            ],
        }
    
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    def validate_phone(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate phone value."""
        
        requested_slot = tracker.get_slot("requested_slot")
        phone_slot = tracker.get_slot("phone")

        phone_value = None
        if requested_slot == "phone":
            phone_value = value.replace('-','').replace(' ','')
            
            pkl_db = './persons.pkl'
            if path.exists(pkl_db):
                df = pd.read_pickle(pkl_db)
                if phone_value in df.index:
                    dispatcher.utter_message(text="פרטיך נטענו בהצלחה, ברוכים השבים %s" % df.loc[phone_value].username)
                    return { 'phone': phone_value,
                             'username': df.loc[phone_value].username,
                             'gender': df.loc[phone_value].gender,
                             'age': df.loc[phone_value].age,
                             'weight': df.loc[phone_value].weight,
                             'height': df.loc[phone_value].height }
            else:
                df = pd.DataFrame(columns=["username", "gender", "age", "weight", "height"])
                df.to_pickle(pkl_db)
        elif phone_slot:
            phone_value = phone_slot
           
        return {"phone": phone_value}
    
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    def validate_username(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate username value."""
        
        requested_slot = tracker.get_slot("requested_slot")
        username_slot = tracker.get_slot("username")

        username_value = None
        if requested_slot == "username":
            username_value = value
        elif username_slot:
            username_value = username_slot

        return {"username": username_value}
    
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    def validate_gender(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate gender value."""
        
        requested_slot = tracker.get_slot("requested_slot")
        gender_slot = tracker.get_slot("gender")

        gender_value = None
        if requested_slot == "gender":
            gender_value = value
        elif gender_slot:
            gender_value = gender_slot

        return {"gender": gender_value}
  
    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    def validate_age(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate age value."""
        
        requested_slot = tracker.get_slot("requested_slot")
        age_slot = tracker.get_slot("age")

        age_value = None
        if requested_slot == "age":
            age_value = value
        elif age_slot:
            age_value = age_slot

        return {"age": age_value}

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    def validate_weight(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate weight value."""
        
        requested_slot = tracker.get_slot("requested_slot")
        weight_slot = tracker.get_slot("weight")
        
        weight_value = None
        if requested_slot == "weight":
            weight_value = value
        elif weight_slot:
            weight_value = weight_slot

        return {"weight": weight_value}

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    def validate_height(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate height value."""
        
        requested_slot = tracker.get_slot("requested_slot")
        height_slot = tracker.get_slot("height")

        height_value = None
        if requested_slot == "height":
            height_value = value
        
            pkl_db = './persons.pkl'
            if path.exists(pkl_db):
                df = pd.read_pickle(pkl_db)
                phone_value = tracker.get_slot("phone")
                if phone_value not in df.index:
                    df.loc[phone_value] = [tracker.get_slot("username"),
                                           tracker.get_slot("gender"),
                                           tracker.get_slot("age"),
                                           tracker.get_slot("weight"),
                                           height_value]
                    df.to_pickle(pkl_db)
                    dispatcher.utter_message(text="פרטיך נרשמו במערכת, לטובת כניסה מהירה יותר בפעם הבאה, תודה.")

        elif height_slot:
            height_value = height_slot
            
        return {"height": height_value}

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """ Define what the form has to do after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(text="מה נעשה היום?")
        return []

