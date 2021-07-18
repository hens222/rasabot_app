# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

import re
import io
import ast
import requests
import numpy as np
import pandas as pd
import random
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk import FormValidationAction
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
import warnings
from statistics import mean
from os import path, getenv
from datetime import datetime
import matplotlib.pyplot as plt
from botocore.exceptions import ClientError
from boto3.exceptions import S3UploadFailedError
import boto3

DB_AWS_ACCESS_KEY_ID = getenv('DB_AWS_ACCESS_KEY_ID')
DB_AWS_SECRET_ACCESS_KEY = getenv('DB_AWS_SECRET_ACCESS_KEY')
DB_AWS_BUCKET = 'journeypic'


# ------------------------------------------------------------------

def upload_file_to_s3(local_file, s3_folder, s3_file, aws_access_key_id, aws_secret_access_key, aws_bucket,
                      debug_en=False):
    """ upload a given file to given location on Amazon-S3 """

    success = True
    HTTP_OK = 200

    # Connect to Amazon-S3 client:
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Make a new directory on S3 (if not already exists):
    if s3_folder + '/' in [x['Key'] for x in s3_client.list_objects(Bucket=aws_bucket)['Contents']]:
        pass
    elif not debug_en:
        res = s3_client.put_object(Bucket=aws_bucket, Key='%s/' % s3_folder)
        success = res['ResponseMetadata']['HTTPStatusCode'] == HTTP_OK
        if not success:
            return success, ""

    # Upload local_file to S3:
    x = 3
    if not debug_en:
        try:
            if path.exists(local_file):
                s3_client.upload_file(local_file, aws_bucket, path.join(s3_folder, s3_file))
                s3_client.put_object_acl(ACL='public-read', Bucket=aws_bucket, Key=path.join(s3_folder, s3_file))
        except (ClientError, S3UploadFailedError) as e:
            success = False, ""

    return success, "https://%s.s3.eu-central-1.amazonaws.com/%s/%s" % (aws_bucket, s3_folder, s3_file)


# ------------------------------------------------------------------

def donut_generator(names, sizes, radius=0.7, textstr_title='',
                    colors=None, figname="image.png"):
    if colors is None:
        colors = []
    my_circle = plt.Circle((0, 0), radius, color='white')
    fig, ax = plt.subplots()

    labels = [':%s\nתוירולק %d' % (k1, k2) for k1, k2 in zip(names, sizes)]

    if colors:
        ax.pie(sizes, colors=colors)
    else:
        ax.pie(sizes)
    plt.legend(bbox_to_anchor=(1.0, 0.88), fontsize=18, labels=labels)
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    if textstr_title:
        ax.text(0.34, 1.05, textstr_title, transform=ax.transAxes, weight='bold',
                fontsize=30, verticalalignment='center_baseline')

    textstr_center1 = str(sum(sizes))
    textstr_center2 = 'קלוריות'[::-1]

    ax.text(0.39, 0.56, textstr_center1, transform=ax.transAxes, weight='bold',
            fontsize=24, verticalalignment='center_baseline')

    ax.text(0.37, 0.44, textstr_center2, transform=ax.transAxes,
            fontsize=18, verticalalignment='center_baseline')

    if figname:
        fig.patch.set_facecolor('white')
        fig.savefig(figname, bbox_inches='tight', facecolor='white')

    else:
        plt.show()


# ------------------------------------------------------------------

def donut_generator_wrapper(title, data):
    names = [x[::-1] for x in list(data.keys())]
    sizes = list(data.values())

    colors = ['darkorange', 'lightgreen', 'blue']

    textstr_title = title[::-1]

    figname = "donut_image1.png"

    donut_generator(names=names,
                    sizes=sizes,
                    radius=0.7,
                    textstr_title=textstr_title,
                    colors=colors,
                    figname=figname)

    return figname


# ------------------------------------------------------------------

def iniliatize_Diagram(title, data):
    unique_filename = lambda fname: "%s_%s%s" % (path.splitext(fname)[0],
                                                 datetime.now().strftime("%m%d%Y_%H%M%S"),
                                                 path.splitext(fname)[1])

    figname = donut_generator_wrapper(title, data)

    res, figure_url = upload_file_to_s3(local_file=figname,
                                        s3_folder="auto_generated",
                                        s3_file=unique_filename(figname),
                                        aws_access_key_id=DB_AWS_ACCESS_KEY_ID,
                                        aws_secret_access_key=DB_AWS_SECRET_ACCESS_KEY,
                                        aws_bucket=DB_AWS_BUCKET)
    return figure_url


# ------------------------------------------------------------------

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
                                              "action_nutrition_bloodtest_value",
                                              "action_nutrition_food_substitute",
                                              "action_nutrition_compare_foods",
                                              "action_nutrition_howmanyxyinz"]).fillna(0)

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
                                          usecols=["nutrition_density", "energy_density",
                                                   "description_density"]).fillna(0)

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
                                             usecols=["Nutrient", "Medium - threshold per 100gr",
                                                      "High - threshold per 100gr",
                                                      "good_or_bad", "tzameret_name", "hebrew_name"]).fillna(0)

    # "Newt Machine Readable" - MicroNutrients
    if (db_bitmap & 0x40) > 0:
        url = "https://docs.google.com/spreadsheets/d/1IPTflCe6shaP-FBAuXWSFCX5hSuAo7bMGczNMTSTYY0/export?format=csv&gid=222801095"
        s = requests.get(url).content
        micro_nutrients_df = pd.read_csv(io.StringIO(s.decode('utf-8')),
                                         header=0).fillna(0)
        db_dict['micro_nutrients'] = micro_nutrients_df

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

    # "Zameret_hebrew_features" - For Noa
    if (db_bitmap & 0x400) > 0:
        url = "https://docs.google.com/spreadsheets/d/19rYDpki0jgGeNlKLPnINiDGye8QEfQ4IEEWSkLFo83Y/export?format=csv&gid=82221888"
        s = requests.get(url).content
        food_units_features_df = pd.read_csv(io.StringIO(s.decode('utf-8')), header=1)
        db_dict['food_units_features'] = food_units_features_df.dropna(axis=0, how='all')
        db_dict['food_units_features'] = db_dict['food_units_features'].rename({'Primary_SN': 'smlmitzrach'},
                                                                               axis=1)

    # "Zameret_hebrew_features" - subs_tags_alias
    if (db_bitmap & 0x800) > 0:
        url = "https://docs.google.com/spreadsheets/d/1VvXmu5l58XwcDDtqz0bkHIl_dC92x3eeVdZo2uni794/export?format=csv&gid=458428667"
        s = requests.get(url).content
        db_dict['subs_tags_alias'] = pd.read_csv(io.StringIO(s.decode('utf-8')),
                                                 header=0,
                                                 usecols=["Entity Alias", "Entity", "Show_stopers"]).set_index(
            'Entity Alias')

    return db_dict


# ------------------------------------------------------------------

def import_sheets(debug=False):
    '''Import the df noa and tzameret food group tabs from the suggested meal planning sheet as a DataFrame. Import weights and measures, and tzameret food list from Tzameret DB as a DataFrame'''

    sheet_id = '19rYDpki0jgGeNlKLPnINiDGye8QEfQ4IEEWSkLFo83Y'

    # import seperalty
    gid_2 = '428717261'
    df_tzameret_food_group = pd.read_csv(
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid_2}")

    df = load_db(0x481)
    df_nutrition = df['tzameret']
    df_nutrition.fillna(0, inplace=True)
    df_nutrition.rename(columns={'carbohydrates': 'carbs'}, inplace=True)
    df_weights = df['food_units']
    df_weights.head()
    df_noa_pre_1 = df['food_units_features']

    df_noa = df['food_units_features']
    header = list(df_noa_pre_1.columns.values)
    df_noa.loc[-1] = header  # adding a row
    df_noa.index = df_noa.index + 1  # shifting index
    df_noa = df_noa.sort_index()  # sorting by index
    df_noa.head()

    df_noa.columns = df_noa.columns.str.lower()
    df_noa = df_noa.iloc[1:]  # df_noa doesn not have the first row with the numbers to make it easier to filter data
    df_noa['lactose_free'] = df_noa['lactose_free'].replace({'Low Lactose': 'Yes', 'Lactose Free': 'Yes'})
    df_noa['food_category'] = df_noa['food_category'].replace({'N/A': 'Savoury_Snacks'})
    df_noa.dropna(subset=["food_name"],
                  inplace=True)  # dropping all meals that don't have a meal name to get complete list of actual meals

    df_noa = df_noa.rename(columns={'smlmitzrach': 'primary_sn'})

    df_noa['sn_1'] = df_noa['primary_sn'].astype(str).str[:1]
    df_noa['sn_2'] = df_noa['primary_sn'].astype(str).str[1:2]

    return df_noa, df_tzameret_food_group, df_weights, df_nutrition


# ------------------------------------------------------------------

def get_rda(name, tracker, intent_upper=False):
    db_dict = load_db(0x46)

    lut_df = db_dict['lut']
    micro_nutrients_df = db_dict['micro_nutrients']
    if intent_upper:
        micro_nutrients_df = micro_nutrients_df[micro_nutrients_df['Type'] == "Upper Limit"]
    else:
        micro_nutrients_df = micro_nutrients_df[micro_nutrients_df['Type'] == "RDA"]

    status = "match"
    if not (tracker.get_slot('gender') and tracker.get_slot('age') and tracker.get_slot(
            'weight') and tracker.get_slot(
        'height')):
        status = "default"

    nutrient = None
    x = tracker.get_slot('x') if tracker.get_slot('x') else None
    if x is not None and x is not "":
        nutrient = x
    else:
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
                                     ((micro_nutrients_df['Gender'] == "ANY") | (
                                             micro_nutrients_df['Gender'] == gender)) & \
                                     ((micro_nutrients_df['Pregnancy'] == "ANY") | (
                                             micro_nutrients_df['Pregnancy'] == "No")) & \
                                     ((micro_nutrients_df['Lactating'] == "ANY") | (
                                             micro_nutrients_df['Lactating'] == "No")) & \
                                     ((micro_nutrients_df['Age Min'] == "ANY") | (
                                             micro_nutrients_df['Age Min'].astype(float) <= int(
                                         user_vars['age']))) & \
                                     ((micro_nutrients_df['Age Max'] == "ANY") | (
                                             micro_nutrients_df['Age Max'].astype(float) > int(user_vars['age'])))]

        rda_text = str(rda_row['Free Text'].values[0])
        rda_value = str(rda_row['Value'].values[0])
        rda_units = rda_row['Units'].values[0]

        if 'slot#' in rda_value:
            rda_value_list = rda_value.split(' ')
            for k, el in enumerate(rda_value_list):
                if 'slot#' in el and el.split('#')[1] in user_vars:
                    rda_value_list[k] = user_vars[el.split('#')[1]]
            rda_value = eval(' '.join(rda_value_list))

        rda_value = float(rda_value)

        if 'slot#' in rda_text:
            rda_text_list = rda_text.split(' ')
            for k, el in enumerate(rda_text_list):
                if 'slot#' in el:
                    rda_text_list[k] = tracker.get_slot(el.split('#')[1])

            rda_text = ' '.join(rda_text_list)

        rda_text_list = re.findall('\{.*?\}', rda_text)
        for match in rda_text_list:
            rda_text = rda_text.replace(match, str(eval(match[1:-1])))

        if rda_text == "0":
            rda_text = ""

        return rda_value, rda_units, rda_text, status, nutrient

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
def how_many_x_in_y_core(x, y, food_units, name, tracker):
    db_dict = load_db(0x293)
    y_common = y
    if y in db_dict['common_food'].index:
        y_common = db_dict['common_food'][db_dict['common_food'].index == y]['shmmitzrach'][0]
    else:
        y_food = ' '.join(y.split(' ')[1:])
        food_units = db_dict['food_units_aliases'][db_dict['food_units_aliases']['Unit Alias'] == y.split(' ')[0]][
            'Zameret unit']
        if food_units.empty:
            food_units = y.split(' ')[0]
        else:
            food_units = food_units.values[0]
        if y_food in db_dict['common_food'].index:
            y_common = db_dict['common_food'][db_dict['common_food'].index == y_food]['shmmitzrach'][0]
        else:
            y_common = y_food

    food = db_dict['tzameret'][db_dict['tzameret']['shmmitzrach'].str.contains(y_common)].iloc[0, :]
    feature = db_dict['lut'][db_dict['lut'].index == x]["Entity"][0]
    units = db_dict['lut'][db_dict['lut'].index == x]["Units"][0]

    food_units_row = pd.Series()
    if food_units:
        food_units_row = db_dict['food_units'][(db_dict['food_units']['smlmitzrach'] == int(food['smlmitzrach'])) &
                                               (db_dict['food_units']['shmmida'] == food_units)]

    is_food_units_match = not food_units_row.empty or food_units == "100 גרם"

    food_units_factor = 1.0
    if not food_units_row.empty:
        food_units_factor = food_units_row['mishkal'].values[0] / 100

    val = food[feature] * food_units_factor

    if units == 0:
        res = "ב-%s של %s יש %.2f %s" % (food_units, food['shmmitzrach'], float(val), x)
    else:
        res = ""
        if not is_food_units_match:
            res = "לא הצלחתי למצוא נתונים במאגר על היחידה %s עליה שאלת\n" % food_units
            res += "היחידות הבאות קיימות במאגר, עבור %s:\n" % food['shmmitzrach']
            res += ', '.join(db_dict['food_units'][db_dict['food_units']['smlmitzrach'] == int(food['smlmitzrach'])][
                                 'shmmida'].to_list())
            res += "\n"
            food_units = "100 גרם"

        res += "ב-%s של %s יש %.2f %s %s" % (food_units, food['shmmitzrach'], float(val), units, x)

    rda_val, rda_units, rda_text, rda_status, nutrient = get_rda(name, tracker)

    if rda_val > 0 and units not in ['יחב"ל']:  # FIXME: unsupported units
        rda = 100 * float(val) / rda_val
        res += "\n"
        res += "שהם כ-%d אחוז מהקצובה היומית המומלצת %s" % (int(rda), get_personal_str(rda_status, tracker))

    if rda_text and rda_text != '0':
        res += '\n' + rda_text

    return val, res


# ------------------------------------------------------------------
#  ____        _ _     _    __  __            _
# | __ ) _   _(_) | __| |  |  \/  | ___  __ _| |
# |  _ \| | | | | |/ _` |  | |\/| |/ _ \/ _` | |
# | |_) | |_| | | | (_| |  | |  | |  __/ (_| | |
# |____/ \__,_|_|_|\__,_|  |_|  |_|\___|\__,_|_|

# Dictionary that is equivalent to user inputs and filters the df_noa Database based on the inputs
def arrayToString(s):
    return ' '.join([str(elem) for elem in s])


def checkDoublePattern(sentence, pattern):
    temp = sentence.count(pattern)
    if temp == 2:
        return sentence[:sentence.find(pattern) + len(pattern)]
    return sentence


def update_budgets(daily_budget, meals_num, snacks_num, weights):
    '''Takes total budget, number of meals and snacks, and weights as paramters. Returns budget for each category for every meal'''
    # change 0.3 to a user params
    budgets = {}
    div = (meals_num + inputs.get(
        'budget_var') * snacks_num)  # Is this supposed to be budget_var(0.3) times snacks num or budget_var times meals_num
    if div > 0:
        budgets['meal'] = round(daily_budget / div, 1)
        budgets['snack'] = round(inputs.get('budget_var') * daily_budget / div, 1)
        budgets['Carbs'] = round(weights[0] * budgets['meal'], 1)
        budgets['Protein'] = round(weights[1] * budgets['meal'], 1)
        budgets['Vegetables'] = round(weights[2] * budgets['meal'], 1)
        budgets['Fruits'] = round(weights[3] * budgets['snack'], 1)
        budgets['Fat'] = round(weights[4] * budgets['snack'], 1)
        budgets['Fat_meal'] = round(weights[4] * budgets['meal'], 1)
        budgets['Savoury_Snacks'] = round(weights[5] * budgets['snack'], 1)
        budgets['Sweets'] = round(weights[6] * budgets['snack'], 1)
        budgets['all'] = round(daily_budget, 1)

    return budgets


def filter_meals_by_features(user_params, df_feature):
    '''Takes user inputs and a Dataframe as parameters and returns a DataFrame filtered by the user inputs'''
    for k, v in user_params.items():
        if (v == 'Yes') and (debug['debug_en']):
            df_feature = df_feature.loc[df_feature[k] == v]
    return df_feature


def filter_meals_by_meal_type(df, meal_type):
    '''Filters the DataFrame by the meal type to be used in making a scoreboard for each meal like breakfast, lunch etc.'''

    if debug:
        return df.loc[(df['il_' + meal_type] == 'Yes')]


def candidate_units_amounts(item, sn, items_type):
    '''Returns the different options for mida amount and servings for each amount'''

    sn_1 = int(item['sn_1'].values[0])
    df_max_meal = df_tzameret_food_group.loc[df_tzameret_food_group['ספרה ראשונה בקוד'] == sn_1]
    units_intersection = []
    amounts_intersection = []
    if items_type != 'snack':
        df_max_meal = df_tzameret_food_group.loc[df_tzameret_food_group['ספרה ראשונה בקוד'] == sn_1]
        max_amount_meal = df_max_meal['mida_maxAmount_meal'].values[0].replace(' ', '').split(',')
        df_weights_list = df_weights[df_weights['smlmitzrach'] == sn]
        weights_list = df_weights_list['mida'].tolist()
        max_amount_meal_units = [int(value.split('_')[0]) for value in max_amount_meal]
        max_amount_meal_amounts = [list(range(1, int(value.split('_')[1]) + 1)) for value in max_amount_meal]
        for k, value in enumerate(max_amount_meal_units):
            if value in weights_list:
                units_intersection.append(value)
                amounts_intersection.append(max_amount_meal_amounts[k])
    else:
        max_amount_snack = df_max_meal['mida_maxAmount_snack'].values[0].replace(' ', '').split(',')
        df_weights_list = df_weights[df_weights['smlmitzrach'] == sn]
        weights_list = df_weights_list['mida'].tolist()
        max_amount_snack_units = [int(value.split('_')[0]) for value in max_amount_snack]
        max_amount_snack_amounts = [list(range(1, int(value.split('_')[1]) + 1)) for value in max_amount_snack]
        for k, value in enumerate(max_amount_snack_units):
            if value in weights_list:
                units_intersection.append(value)
                amounts_intersection.append(max_amount_snack_amounts[k])
    return units_intersection, amounts_intersection


def get_item_property(sn, grams, serving):
    '''Returns the total item calories for each item'''

    # if the mida is 700 then multiply by 100, if any other number divide by 100
    weights = df_weights[(df_weights['smlmitzrach'] == sn) & (df_weights['mida'] == grams)]
    mishkal = weights.iloc[0]['mishkal']
    if mishkal == 700:
        mishkal = mishkal * 100
    else:
        mishkal = mishkal / 100
    attribute = df_nutrition.loc[df_nutrition['smlmitzrach'] == str(int(sn))]
    attribute_total = attribute.iloc[0]['food_energy']
    total = attribute_total * mishkal * serving

    return total, weights.iloc[0]['shmmida'], weights.iloc[0]['mishkal'], weights, serving


def update_calorie_budgets(candidate_calories, item_type, bud):
    '''Updates the calories budget based on how many calories were already used'''

    bud[item_type] = bud[item_type] - candidate_calories
    return bud


def build_meal(meals_bank, meal_type, budget):
    # make histogram without penalty score of runnning the simulator 50 times and picking the winners. Run it again with the penalty score
    '''Builds a meal taking a DataFrame, meal type and budget as parameters. Meal takes item from each category (Carbs, Protein etc.) and returns the meal, weighted average score and total meal calories'''
    budget_weights = {**budget_weights_meals, **budget_weights_snacks_fruits_fat, **budget_weights_savoury_snacks,
                      **budget_weights_sweets}
    bud = {}
    meal_similarity_list = []
    df_health = df_nutrition.iloc[1:]
    max_meal_items = inputs.get('max_items_snack') if meal_type == 'snack' else inputs.get('max_items_meal')
    nutrition_density_list = []
    energy_density_list = []
    meal_score = 0
    score_list = []
    uti_score = []
    ind_score = []
    score = 0
    meals = []
    meal_cals = 0
    types = []
    total_budget = budget.copy()
    item_types = {'breakfast': ['Carbs', 'Protein', 'Vegetables'],
                  'lunch': ['Carbs', 'Protein', 'Vegetables'],
                  'dinner': ['Carbs', 'Protein', 'Vegetables'],
                  'snack': ['Fat']}
    if (snacks.get('sweets') == 'Yes') & (len(meals_bank.loc[meals_bank['food_category'] == 'Sweets']) > 0):
        item_types['snack'].append('Sweets')
    if (snacks.get('Savoury_Snacks') == 'Yes') & (
            len(meals_bank.loc[meals_bank['food_category'] == 'Savoury_Snacks']) > 0):
        item_types['snack'].append('Savoury_Snacks')
    if (user_params.get('fruits') == 'No') & (len(meals_bank.loc[meals_bank['food_category'] == 'Fruits']) > 0):
        item_types['snack'].append('Fruits')
    for k in range(max_meal_items):
        for item_type in item_types[meal_type]:
            success = False
            if (len(meals_bank.loc[meals_bank['food_category'] == item_type]) > 0):
                df = meals_bank.loc[meals_bank['food_category'] == item_type].sample()
            candidate_units = candidate_units_amounts(df, int(df['primary_sn'].values[0]), item_type)
            candidate_grams = candidate_units[0]
            for can_grams in candidate_grams:
                sn = float(df['primary_sn'].values[0])
                for candidate_amount in candidate_units[1]:
                    for amount in reversed(candidate_amount):
                        calories, weight, grams, x, y = get_item_property(sn, can_grams, amount)
                        can_cals = getattr(calories, "tolist", lambda: candidate_calories)()
                        if can_cals < budget[item_type]:
                            success = True
                            if success:
                                if success:
                                    sn_int = int(df['primary_sn'].astype(str).str[:1])
                                    sn1 = float(df['primary_sn'].values[0])
                                    calories1, weight, grams, x, y = get_item_property(sn1, can_grams, amount)
                                    bud[item_type] = getattr(calories1, "tolist", lambda: candidate_calories)()
                                    units_priority = candidate_grams.index(can_grams) + 1
                                    meal_score += 1 / units_priority
                                    df_sn1 = df_tzameret_food_group.loc[
                                        df_tzameret_food_group['ספרה ראשונה בקוד'] == sn_int]
                                    df_fish = df_noa.loc[df_noa['primary_sn'] == sn1]
                                    food_group = df_sn1['קבוצת המזון']
                                    if sn_int == 2:
                                        if df_fish['fish_free'].iloc[0] == 'Yes':
                                            meal_similarity_list.append(2.1)
                                        else:
                                            meal_similarity_list.append(2.2)
                                    else:
                                        meal_similarity_list.append(sn_int)
                                    item_score = (bud[item_type]) / (budget[item_type])
                                    df['score'] = item_score
                                    score_list.append(item_score)
                                    types.append(df['food_category'])
                                    nutrition_density_normalized = df_nutrition.loc[
                                        df_nutrition['smlmitzrach'] == str(
                                            int(sn1)), 'Nutrition density normalized']
                                    energy_density = df_health.loc[
                                        df_health['smlmitzrach'] == str(int(sn1)), 'Energy density']
                                    nutrition_density_normalized = nutrition_density_normalized.astype(float)
                                    energy_density = energy_density.astype(float)
                                    dataframe = df[['food_name', 'primary_sn']]
                                    dataframe.insert(2, 'Weight', [grams])
                                    dataframe.insert(3, 'Unit', [weight])
                                    dataframe.insert(4, 'Amount', [amount])
                                    meals.append(dataframe)
                                    nutrition_density_list.append(nutrition_density_normalized.values.tolist())
                                    energy_density_list.append(energy_density.values.tolist())
                                    meal_cals = meal_cals + calories1
                                    budget = update_calorie_budgets(can_cals, item_type, budget)
                                break
                    if success or budget[item_type] < units_thr[item_type] or len(meals) >= max_meal_items:
                        break
                if success or budget[item_type] < type_thr[item_type] or len(meals) >= max_meal_items:
                    break
            if budget['all'] < inputs['item_thr'] or len(meals) >= max_meal_items:
                break
        if len(meals) >= max_meal_items:
            break
    types_list_no_duplicates = np.unique([x.values[0] for x in types]).tolist()
    for each_type in reversed(types_list_no_duplicates):
        each_score = (float(total_budget.get(each_type)) - float(budget.get(each_type))) / float(
            total_budget.get(each_type))
        ind_score.append(each_score)
        uti_score.append(budget_weights.get(each_type))
    if (len(ind_score) < len(item_types[meal_type])):
        ind_score.append(0.000001)
        uti_score.append(.35)
    if (min(ind_score) < 0.7) and (meal_type != 'snack'):
        extra_penalty = inputs.get('extra_penalty')
    else:
        extra_penalty = 0
    if (len(meals)) > 4:
        meal_penalty_length = (len(meals) - 4) * inputs.get('meal_penalty_length')
    else:
        meal_penalty_length = 0
    total_utilization = sum(x * y for x, y in zip(ind_score, uti_score)) / sum(uti_score)

    if len(meal_similarity_list) != len(set(meal_similarity_list)):
        meal_similarity_penalty = inputs.get('meal_similarity_penalty')
    else:
        meal_similarity_penalty = 0
    nutrition_density_list = [float(x) for [x] in nutrition_density_list]
    try:
        avg_nutrition = round(mean(nutrition_density_list), 4)
    except:
        avg_nutrition = nutrition_density_list
    energy_density_list = [float(x) for [x] in energy_density_list]
    avg_energy = round(mean(energy_density_list), 4)

    penalty_score = 1 - meal_score / len(meals)
    nutrition_boost = avg_nutrition * inputs.get('nutrition_bonus')
    energy_boost = avg_energy * inputs.get('energy_bonus')
    if scoring.get('legacy'):
        score = total_utilization - (
                penalty_score * inputs.get('penalty_weight')) - extra_penalty - meal_penalty_length
    elif scoring.get('legacy_nut'):
        score = total_utilization - (penalty_score * inputs.get(
            'penalty_weight')) - extra_penalty - meal_penalty_length + nutrition_boost
    elif scoring.get('legacy_ene'):
        total_utilization - (
                penalty_score * inputs.get('penalty_weight')) - extra_penalty - meal_penalty_length + energy_boost
    else:
        score = total_utilization - (penalty_score * inputs.get(
            'penalty_weight')) - extra_penalty - meal_penalty_length + energy_boost + nutrition_boost
    return meals, score, meal_cals, ind_score, meal_penalty_length, avg_nutrition, avg_energy, meal_similarity_penalty, meal_similarity_list


def build_meal_wrapper():
    energy_density_listy = 0.0
    meal_similarity_listy = []
    nutrition_density_listy = []
    meal_similarity_penaltyy = []
    nutrition_density_listx = []
    energy_density_listx = 0.0
    meal_similarity_penaltyx = []
    meal_similarity_listx = []
    penalty_lengthy = []
    # Builds and populates a scoreboard that sorts the meals based on their score
    x = -3
    pd.set_option('precision', 2)
    max_iterations = inputs.get('max_iter')
    budget_weights = {**budget_weights_meals, **budget_weights_snacks_fruits_fat, **budget_weights_savoury_snacks,
                      **budget_weights_sweets}
    budget_weights_list = []

    for k, v in budget_weights.items():
        budget_weights_list.append(v)

    score_tracker = -2
    total_cals = 0

    meals = {}
    user_meals_num = inputs.get('meals_num')
    user_snacks_num = inputs.get('snacks_num')
    filler = []
    meal_types = ['breakfast', 'lunch', 'dinner']
    for k in range(inputs.get('snacks_num')):
        meal_types.append('snack')

    features = filter_meals_by_features(user_params, df_noa)
    for meal_type in meal_types:
        bank = filter_meals_by_meal_type(features, meal_type)
        x += 1
        scoreboard = {}
        for k in range(inputs.get('max_iter')):
            budgets_dynamic = update_budgets(inputs.get('total_cals'), inputs.get('meals_num'),
                                             inputs.get('snacks_num'), budget_weights_list)
            meal_budget = update_budgets(inputs.get('total_cals'), inputs.get('meals_num'),
                                         inputs.get('snacks_num'),
                                         budget_weights_list)

            if meal_type != 'snack':
                mealy, scorey, calsy, ut_scorey, penalty_lengthy, nutrition_density_listy, energy_density_listy, meal_similarity_penaltyy, meal_similarity_listy = build_meal(
                    bank, meal_type, budgets_dynamic)

                if mealy and scorey and min(ut_scorey) > 0:
                    scoreboard[meal_type] = mealy, scorey, calsy
                    if scoreboard[meal_type][1] > score_tracker:
                        score_tracker = scoreboard[meal_type][1]
                        total_cals = scoreboard[meal_type][2]


            else:
                mealx, scorex, calsx, ut_scorex, penalty_lengthx, nutrition_density_listx, energy_density_listx, meal_similarity_penaltyx, meal_similarity_listx = build_meal(
                    bank, meal_type, meal_budget)
                if mealx:
                    scoreboard[
                        meal_type] = mealx, scorex, calsx, nutrition_density_listx, energy_density_listx, meal_similarity_penaltyx, meal_similarity_listx

            if scoreboard:
                meals[meal_type] = scoreboard[meal_type]

            for meal_name, whole_meal in scoreboard.items():
                df = pd.concat(whole_meal[0])
                df = pd.DataFrame(df.values.reshape(1, -1))
                df['score'] = float(scoreboard[meal_type][1])
                df['meal_cals'] = scoreboard[meal_type][2]
                if meal_name != 'snack':
                    df['name'] = meal_name
                    df['budget per meal'] = meal_budget.get('meal')
                    df['meal budget utilization'] = (df['meal_cals'] / df['budget per meal'])
                    df['average nutrtition'] = nutrition_density_listy
                    df['average energy'] = energy_density_listy
                    df['meal_similarity_penalty'] = meal_similarity_penaltyy
                    df['meal_similarity_list'] = pd.Series([meal_similarity_listy])
                    df.set_index('name', drop=True, inplace=True)
                else:
                    df['name'] = meal_name + " " + str(x)
                    df['budget per snack'] = budgets_dynamic.get('snack')
                    df['snack budget utilization'] = (df['meal_cals'] / df['budget per snack'])
                    df['average nutrtition'] = nutrition_density_listx
                    df['average energy'] = energy_density_listx
                    df['meal_similarity_penalty'] = meal_similarity_penaltyx
                    df['meal_similarity_list'] = pd.Series([meal_similarity_listx])
                    df.set_index('name', drop=True, inplace=True)

                if meal_name != 'snack':
                    # rename all the budget as budget leftover so its carbs budget leftover etc.
                    df['meal penalty length'] = penalty_lengthy
                    df['carb budget per meal'] = int(meal_budget.get('Carbs'))
                    df['carbs budget remaining'] = budgets_dynamic.get('Carbs')
                    df['carb budget utilization'] = (meal_budget.get('Carbs') - budgets_dynamic.get(
                        'Carbs')) / meal_budget.get('Carbs')
                    df['protein budget per meal'] = meal_budget.get('Protein')
                    df['protein budget remaining'] = budgets_dynamic.get('Protein')
                    df['protein budget utilization'] = (meal_budget.get('Protein') - budgets_dynamic.get(
                        'Protein')) / meal_budget.get('Protein')
                    df['vegetable budget per meal'] = meal_budget.get('Vegetables')
                    df['vegetable budget remaining'] = budgets_dynamic.get('Vegetables')
                    df['vegetable budget utilization'] = (meal_budget.get('Vegetables') - budgets_dynamic.get(
                        'Vegetables')) / meal_budget.get('Vegetables')
                    df['fat budget per meal'] = meal_budget.get('Fat_meal')
                    df['fat budget remaining'] = budgets_dynamic.get('Fat_meal')
                    df['fat budget utilization'] = (meal_budget.get('Fat_meal') - budgets_dynamic.get(
                        'Fat_meal')) / meal_budget.get('Fat_meal')


                else:
                    if snacks.get('sweets') == "Yes":
                        df['sweets budget per snack'] = meal_budget.get('Sweets')
                        df['sweets budget remaining'] = budgets_dynamic.get('Sweets')
                        df['sweets budget utilization'] = (meal_budget.get('Sweets') - budgets_dynamic.get(
                            'Sweets')) / meal_budget.get('Sweets')
                    if snacks.get('Savoury_Snacks') == 'Yes':
                        df['savoury budget per snack'] = meal_budget.get('Savoury_Snacks')
                        df['savoury budget remaining'] = budgets_dynamic.get('Savoury_Snacks')
                        df['savoury budget utilization'] = (meal_budget.get('Savoury_Snacks') - budgets_dynamic.get(
                            'Savoury_Snacks')) / meal_budget.get('Savoury_Snacks')
                    if user_params.get('fruits') == 'No':
                        df['fruits budget per snack'] = meal_budget.get('Fruits')
                        df['fruits budget remaining'] = budgets_dynamic.get('Fruits')
                        df['fruits budget utilization'] = (meal_budget.get('Fruits') - budgets_dynamic.get(
                            'Fruits')) / meal_budget.get('Fruits')
                    df['fat budget per snack'] = meal_budget.get('Fat')
                    df['fat budget remaining'] = budgets_dynamic.get('Fat')
                    df['fat budget utilization'] = (meal_budget.get('Fat') - budgets_dynamic.get(
                        'Fat')) / meal_budget.get('Fat')
            filler.append(df)
        if meal_type == 'snack':
            user_snacks_num -= 1
        else:
            user_meals_num -= 1
        budgets_dynamic = update_budgets(float(inputs.get('total_cals') - total_cals), user_meals_num, user_snacks_num,
                                         budget_weights_list)

    df_meals = pd.concat(filler)
    df_final = df_meals.sort_values(by=['name', 'score'], ascending=[True, False])

    df_final.rename(columns={0: "Item 1", 1: "Primary SN 1", 2: "Weight", 3: "Unit1", 4: "Amount1",
                             5: "Item 2", 6: "Primary SN 2", 7: "Weight", 8: "Unit2", 9: "Amount2",
                             10: "Item 3", 11: "Primary SN 3", 12: "Weight", 13: "Unit3", 14: "Amount3",
                             15: "Item 4", 16: "Primary SN 4", 17: "Weight", 18: "Unit4", 19: "Amount4"}
                    , inplace=True)

    return df_final


def displayMeal(data, mealType, items_meal_number, sncack_numbers):
    menu = ""
    calories = 0
    # hole day menu
    carbs = 0
    protein = 0
    vegetable = 0
    if len(mealType) > 1:
        for meal in mealType:
            items, temp_calories, temp_carbs, temp_protein, temp_vegetable = getMeal(data, meal, items_meal_number)
            calories += temp_calories
            menu = menu + items
            carbs = carbs + temp_carbs
            protein = protein + temp_protein
            vegetable = vegetable + temp_vegetable
    # one meal for the user
    else:
        menu, calories, carbs, protein, vegetable = getMeal(data, mealType[0], items_meal_number)
        return menu, carbs, protein, vegetable

    snacks, calories_sn = getSnack(data, sncack_numbers)
    menu = menu + snacks
    calories += calories_sn
    menu = menu + "סך הכל קלוריות -> " + arrayToString(str(calories))
    return menu, carbs, protein, vegetable


def getMeal(data, meal_type, meal_items_nubmer):
    # item[0]-> food name
    # item[1]-> unit
    # item[2]-> amount
    dic = {'breakfast': 'ארוחת בוקר', 'lunch': 'ארוחת צהריים', 'dinner': 'ארוחת ערב'}
    temp_meal = data[data.index == meal_type]
    items = get_items(temp_meal, meal_items_nubmer)
    calories = temp_meal['meal_cals'].head(1).values
    # calulate the Nutritional values of the meal
    carbs = temp_meal['carb budget per meal'].head(1).values * temp_meal['carb budget utilization'].head(1).values
    protein = temp_meal['protein budget per meal'].head(1).values * temp_meal['protein budget utilization'].head(
        1).values
    vegetables = temp_meal['vegetable budget per meal'].head(1).values * temp_meal['vegetable budget utilization'].head(
        1).values
    carbs = int(carbs)
    protein = int(protein)
    vegetables = int(vegetables)
    calories = int(calories)

    if meal_items_nubmer == 4:
        return "*" + dic[meal_type] + "*:\n1. " + buildItem(items['item1']) + "\n2. " + buildItem(
            items["item2"]) + "\n3. " + buildItem(
            items['item3']) + "\n4. " + buildItem(
            items['item4']) + "\nכמות קלוריות ->" + str(calories) + "\n\n", calories, carbs, protein, vegetables

    return "*" + dic[meal_type] + "*:\n1. " + buildItem(items['item1']) + "\n2. " + buildItem(
        items["item2"]) + "\n3. " + buildItem(
        items['item3']) + "\nכמות קלוריות ->" + str(calories) + "\n\n", calories, carbs, protein, vegetables


def get_items(temp_meal, items_number):
    meal = {}
    for index in range(1, items_number + 1):
        meal['item' + str(index)] = [temp_meal['Item ' + str(index)].head(1).values,
                                     temp_meal['Unit' + str(index)].head(1).values,
                                     temp_meal['Amount' + str(index)].head(1).values]
    return meal


def getSnack(snackData, snack_number):
    # get the line of each snack
    snack1 = snackData[snackData.index == "snack 1"]
    snack2 = snackData[snackData.index == "snack 2"]
    # get the items
    snack1_ = get_items(snack1, snack_number)
    snack2_ = get_items(snack2, snack_number)
    snack1_calories = snack1['meal_cals'].head(1).values
    snack2_calories = snack2['meal_cals'].head(1).values
    snack1_calories = int(snack1_calories)
    snack2_calories = int(snack2_calories)
    if snack_number == 2:
        return "*ארוחות ביניים 1*:\n1. " + buildItem(snack1_['item1']) + "\n2. " + buildItem(
            snack1_['item2']) + "\n\n*ארוחות ביניים 2*:\n1." + buildItem(snack2_['item1']) + "\n2. " + buildItem(
            snack2_['item2']) + "\nכמות קלוריות -> " + str(
            snack1_calories + snack2_calories) + "\n\n", snack1_calories + snack2_calories
    return "*ארוחות ביניים *:\n1. " + buildItem(snack1_['item1']) + "\n2. " + buildItem(
        snack2_['item1']) + "\nכמות קלוריות -> " + str(
        snack1_calories + snack2_calories) + "\n\n", snack1_calories + snack2_calories


def buildItem(item):
    if item[0] is not 'NaN' and item[2] is not 'Nan' and item[0] is not 'nan' and item[2] is not 'nan':
        item_temp=arrayToString(item[1])
        return arrayToString(item[0]) + " " + arrayToString(item[2]) + " " + unitHebrew(item_temp,item[2])

def unitHebrew(unit, amount):
    unit_dic = {"כף": 'כפות', "מנה": 'מנות', "יחידה קטנה": 'יחידות קטנות', "פרח": 'פרחים',
                "פרוסה בינונית": 'פרוסות בינונוית',
                "יחידה": 'יחידות', "כף גדושה": 'כפות גדושות',
                "פרוסה": 'פרוסות', "מנה קטנה": 'מנות קטנות', "יחידה בינונית": 'יחידות בינוניות', "כפית": 'כפיות',
                "כוס": 'כוסות', "כוס קצוץ": 'כוסות'}
    if unit not in unit_dic:
        return unit

    if amount > 1:
        unit_temp = unit_dic[unit].strip()
        if unit_temp.count(' ') == 1:
            return unit_temp
        unit_temp = unit_temp.replace('  ', '')
        unit_temp = unit_temp.replace(' ', '')
        unit_temp = unit_temp[:unit_temp.find('ת') + 1] + ' ' + unit_temp[unit_temp.find('ת') + 1:]
        # one word
        if unit_temp.count('ת') == 1:
            return unit_temp.strip()
        return unit_temp

    return unit


def core_fun(meal_type, title=""):
    global snacks, user_params, units_thr, type_thr, budget_weights_meals, budget_weights_snacks_fruits_fat, budget_weights_savoury_snacks, budget_weights_sweets, inputs, display_user_parameter, debug

    global user_meals_num, total_cals, user_snacks_num, candidate_calories, scoring

    global df_noa, df_tzameret_food_group, df_weights, df_nutrition
    pd.set_option("display.precision", 2)

    warnings.filterwarnings("ignore")

    # Dictionary that is equivalent to user inputs and filters the df_noa Database based on the inputs
    user_params = {'eggs': 'No',  # If eggs = Yes, filters out all the meals with eggs
                   'vegetables': 'No',  # If vegetables = Yes, fiters out all meals with vegetables
                   'fruits': 'No',
                   # If fruits = Yes, filters out all snacks and meals with fruits and snacks don't have fruits as a category
                   'dairy': 'No',  # If dairy = Yes, filters out all the dairy items
                   'beef_chicken_fish': 'No',
                   # If beef_chicken_fish = Yes, filters out all the meals with beef chicken or fish
                   # For remaining if Yes, filters only the food its for (i.e if kosher = Yes, only shows kosher food)
                   'kosher': 'Yes',
                   'halal': 'Yes',
                   'vegetarian': 'No',
                   'vegan': 'No',
                   'ketogenic': 'No',
                   'paleo': 'No',
                   'mediterranean': 'No',
                   'lactose_free': 'No',
                   'gluten_free': 'No',
                   'milk_free': 'No',
                   'wheat_free': 'No',
                   'egg_free': 'No',
                   'soy_free': 'No',
                   'tree_nut_free': 'No',
                   'peanut_free': 'No',
                   'fish_free': 'No',
                   'shellfish_free': 'No'}
    # Dictionary to see if want to add certain snack elements to the snacks on the scoreboard
    snacks = {'sweets': 'No',
              'Savoury_Snacks': 'Yes'}

    # Threshold for the build meal to stop looking for another item (If there are only 20 Carb calories left the meal exits the Carb code and moves to Protein):
    units_thr = {'Carbs': 25,
                 'Protein': 10,
                 'Vegetables': 10,
                 'Fat': 25,
                 'Fruits': 25,
                 'Sweets': 25,
                 'Savoury_Snacks': 25}

    # Another threshold for build meal to stop looking for another item in the category if there is less budget than the threshold:
    type_thr = {'Carbs': 25,
                'Protein': 10,
                'Vegetables': 10,
                'Fat': 25,
                'Fruits': 25,
                'Sweets': 25,
                'Savoury_Snacks': 25}

    # For snacks its either fruits and fat or savoury or sweets
    budget_weights_meals = {'Carbs': 0.4,
                            'Protein': 0.5,
                            'Vegetables': 0.2}

    budget_weights_snacks_fruits_fat = {'Fruits': 0.7,
                                        'Fat': 0.4}

    budget_weights_savoury_snacks = {'Savoury_Snacks': 1.1}

    budget_weights_sweets = {'Sweets': 1.1}

    scoring = {'legacy': False,  # legacy scoring system composed of budget utilization
               'legacy_nut': True,  # legacy scoring system with a bonus based on average nutritional density
               'legacy_ene': False,  # legacy scroing system with a bonus based on higher energy density
               'legacy_nut_ene': False
               # legacy scoring system with a bonus based on nutrtion density and energy density with higher density the better
               }

    # User inputs that control different variables:
    inputs = {'for_noa_gid': 2106834268,
              # Gid that controls which for noa tab is shown, to switch just paste another Gid
              'budget_var': 0.3,  # Budget variable to see the weighting for snacks and individual meals
              'item_thr': 4,
              # Threshold used to decided when to break code if there is less than 5 total budget left
              'max_items_meal': 4,  # Max amount of items per meal
              'max_items_snack': 2,  # Max amount of items per snack
              'penalty_weight': 1,
              # Penalty weight for the meal score if the meal doesnt take the first option at the intersection of mida max amount meal
              'nutrition_bonus': 0.1,  # Bonus multiplier for the average nutrition density
              'energy_bonus': 0.2,  # Bonus multiplier for the average energy density
              'meal_similarity_penalty': 0.3,
              # Penalty for having mutliple of the same category of meal items in the same meal
              'max_iter': 7,  # Number of meals for each meal type in the scoreboard
              'meals_num': 3,  # Number of different meal types and meals - will always be 3
              'snacks_num': 2,  # number of snacks in the final scoreboard
              'meat_egg_same_day_penalty': 0.2,
              # Peanlty if the top meal has eggs or meat and another meal the same day also has eggs and meat
              'extra_penalty': 0.2,  # Penalty if there is less than 0.7 of each category for the budget is used
              'meal_penalty_length': 0.1,
              # Penalty given if a meal is longer than 4 items and this is the weighting
              'total_cals': 2000  # total calories in the budget for the day
              }

    debug = {'debug_en': True}  # Used for finding bugs in code. Set to True for code to run properly
    # Toggle to show the user values in a DataFrame
    display_user_parameter = {'display_user_parameter': False}

    df_noa, df_tzameret_food_group, df_weights, df_nutrition = import_sheets(False)

    df_main = build_meal_wrapper()
    items, carbs, protein, vegetable = displayMeal(df_main, meal_type, inputs['max_items_meal'],
                                                   inputs['max_items_snack'])

    data = {'חלבון': protein,
            'פחמימות': carbs,
            'ירקות': vegetable}

    url = iniliatize_Diagram(title, data)
    return items, url


# ------------------------------------------------------------------
class Actionhowmanyxyinz(Action):
    def name(self) -> Text:
        return "action_nutrition_howmanyxyinz"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_msg = tracker.latest_message.get('text')
        two_nutrient = None
        z = None
        db_dict = load_db(0x293)
        prediction = tracker.latest_message
        two_nutrient = prediction['entities'][0]['value']
        x, y = two_nutrient.split(' ו')
        x = x.strip()
        y = y.strip()
        regex_res = re.search('כמה (.*) יש ב(.*)', user_msg.replace('?', ''))
        if regex_res:
            if two_nutrient is None:
                x, y = regex_res.group(1)
                x = x.strip()
                y = y.strip()
            z = regex_res.group(2)
        regex_res = re.search('כמה (.*) ב(.*)', user_msg.replace('?', ''))
        if regex_res:
            if two_nutrient is None:
                x, y = regex_res.group(1)
                x = x.strip()
                y = y.strip()
            z = regex_res.group(2)
        regex_res = re.search('מה הכמות של (.*) ב(.*)', user_msg.replace('?', ''))
        if regex_res:
            if two_nutrient is None:
                x, y = regex_res.group(1)
                x = x.strip()
                y = y.strip()
            z = regex_res.group(2)
        y = y[:len(y)]
        # get the units from the user message
        user_msg_temp = user_msg[user_msg.find(two_nutrient) + len(two_nutrient) + 1:len(user_msg)].replace('?', '')
        food1_units = "100 גרם"
        regex_units_res1 = re.search('ב(.*) של', user_msg_temp)
        regex_units_res2 = re.search(' (.*) של', user_msg_temp)
        if regex_units_res1:
            food1_units = regex_units_res1.group(1)
        elif regex_units_res2:
            food1_units = regex_units_res2.group(1)
        if food1_units in db_dict['food_units_aliases']['Unit Alias'].values:
            food1_units = db_dict['food_units_aliases'][db_dict['food_units_aliases']['Unit Alias'] == food1_units][
                'Zameret unit'].values[0]
        try:
            val1, res1 = how_many_x_in_y_core(x, z, food1_units, self.name(), tracker)
            val2, res2 = how_many_x_in_y_core(y, z, food1_units, self.name(), tracker)
            res1 = checkDoublePattern(res1, 'קלוריות')
            res2 = checkDoublePattern(res2, 'קלוריות')
            res = ''
            res += res1
            res += "\n"
            res += res2
        except:
            res = "אין לי מושג כמה, מצטער!"
        dispatcher.utter_message(res)


# ------------------------------------------------------------------

class Actioncompartiontwofoods(Action):
    def name(self) -> Text:
        return "action_nutrition_compare_foods"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message.get('text')
        entities = tracker.latest_message.get('entities')

        x = None
        y1 = None
        y2 = None
        more_or_less = 'יותר' if 'יותר' in user_msg else 'פחות'
        db_dict = load_db(0x293)
        for ent in entities:
            if ent['entity'] in db_dict['lut']["action_nutrition_compare_foods"].values:
                x = ent['value']
            elif ent['entity'] in db_dict['lut']["action_nutrition_compare_foods"].values:
                y1, y2 = ent['value'].split('או')
                y1 = y1.strip()
                y2 = y2.strip()

        if not y1 or not y2:
            y1, y2 = user_msg[user_msg.find(x) + len(x):len(user_msg)].split('או')
            y1 = y1.strip()
            y1 = y1[1:len(y1)]
            y2 = y2.strip()
            if 'בב' in y1:
                y1 = y1[1:len(y1)]
        if not y1 or not y2:
            regex_res = re.search('במה יש (פחות|יותר) .* ב(.*)', user_msg.replace('?', ''))
            if regex_res:
                more_or_less = regex_res.group(1)
                y1, y2 = regex_res.group(2).split('או')
                y1 = y1.strip()
                y2 = y2.strip()

        food1_units = "100 גרם"
        food2_units = "100 גרם"
        for k, y in enumerate([y1, y2]):
            regex_units_res = re.search('(.*) של (.*)', y)
            if regex_units_res:
                if k == 0:
                    food1_units = regex_units_res.group(1)
                    y1 = regex_units_res.group(2)
                else:
                    food2_units = regex_units_res.group(1)
                    y2 = regex_units_res.group(2)

            if food1_units in db_dict['food_units_aliases']['Unit Alias'].values:
                food1_units = db_dict['food_units_aliases'][db_dict['food_units_aliases']['Unit Alias'] == food1_units][
                    'Zameret unit'].values[0]
            if food2_units in db_dict['food_units_aliases']['Unit Alias'].values:
                food2_units = db_dict['food_units_aliases'][db_dict['food_units_aliases']['Unit Alias'] == food2_units][
                    'Zameret unit'].values[0]

        try:
            val1, res1 = how_many_x_in_y_core(x, y1, food1_units, self.name(), tracker)
            val2, res2 = how_many_x_in_y_core(x, y2, food1_units, self.name(), tracker)
            res1 = checkDoublePattern(res1, 'קלוריות')
            res2 = checkDoublePattern(res2, 'קלוריות')
            ys = (y1, y2)
            vals = (val1, val2)
            res = 'ב%s יש %s %s' % (ys[np.argmax(vals) if more_or_less == 'יותר' else np.argmin(vals)], more_or_less, x)
            if 'ב ב' in res and 'בבשר' not in res:
                res = res[1:]
            res += "\n"
            res += res1
            res += "\n"
            res += res2
        except:
            res = "אין לי מושג כמה, מצטער!"

        dispatcher.utter_message(res)


# ------------------------------------------------------------------

class Actionwhataboutx(Action):

    def name(self) -> Text:
        return "action_nutrition_and_what_about_x"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get the right actions according to the intent
        intens_dict = {"nutrition_howmanyxiny": "action_nutrition_howmanyxiny",
                       "nutrition_meal_question": "action_nutrition_meal_question",
                       "nutrition_is_food_healthy": "action_nutrition_is_food_healthy",
                       "nutrition_get_rda": "action_nutrition_get_rda",
                       "nutrition_get_upper_limit": "action_nutrition_get_rda"}
        user_messge = tracker.latest_message.get('text')
        previous_intent = tracker.get_slot('previous_intent')

        try:
            next_action = intens_dict[previous_intent]
            # meal question
            if previous_intent == "nutrition_meal_question":
                return [FollowupAction(next_action), SlotSet("y", ""),
                        SlotSet("x", user_messge), SlotSet("previous_intent", previous_intent)]

            # ------------------------------------------------
            # how many x in y
            if previous_intent == "nutrition_howmanyxiny":
                db_dict = load_db(0x2)
                lut_df = db_dict['lut']
                action_name = "action_nutrition_howmanyxiny"
                y = None
                x = None
                # get the values from the slots
                food = tracker.get_slot('y') if tracker.get_slot('y') else None
                nutriet = tracker.get_slot('x') if tracker.get_slot('x') else None

                # get the entities from the question
                for ent in tracker.latest_message.get('entities'):
                    if ent['entity'] in lut_df[action_name + "_x"].values:
                        x = ent['value']
                    elif ent['entity'] in lut_df[action_name + "_y"].values:
                        y = ent['value']

                if x is None or x == "":
                    x = nutriet
                if y is None or y == "":
                    y = food

                return [FollowupAction(next_action),
                        SlotSet("x", x), SlotSet("y", y),
                        SlotSet("previous_intent", previous_intent)]
            # ------------------------------------------------
            # is x healthy
            if previous_intent == "nutrition_is_food_healthy":
                prediction = tracker.latest_message
                entity_value = prediction['entities'][0]['value']
                return [FollowupAction(next_action),
                        SlotSet("x", entity_value), SlotSet("y", ""),
                        SlotSet("previous_intent", previous_intent)]

            # ------------------------------------------------
            # nutrition_get_rda
            if previous_intent == "nutrition_get_rda":
                prediction = tracker.latest_message
                entity_value = prediction['entities'][0]['value']
                return [FollowupAction(next_action),
                        SlotSet("x", entity_value), SlotSet("y", ""),
                        SlotSet("previous_intent", "nutrition_get_rda")]

            # ------------------------------------------------
            # nutrition_get_upper_limit
            if previous_intent == "nutrition_get_upper_limit":
                prediction = tracker.latest_message
                entity_value = prediction['entities'][0]['value']
                return [FollowupAction(next_action),
                        SlotSet("x", entity_value), SlotSet("y", ""),
                        SlotSet("previous_intent", "nutrition_get_upper_limit")]

        except:
            dispatcher.utter_message(text="אין למושג, מצטער!")
        return []


# ------------------------------------------------------------------

class Actionxcaniny(Action):

    def name(self) -> Text:
        return "action_nutrition_what_xcanbeiny"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            meal = ""
            # loading data frame
            db_dict = load_db(0x402)
            lut = db_dict['lut']
            df_noa = db_dict['food_units_features']

            # get the meal type
            message = tracker.latest_message.get('text')
            if 'בוקר' in message:
                meal = "IL_Breakfast"
            if 'צהריים' in message:
                meal = "IL_Lunch"
            if 'ערב' in message:
                meal = 'IL_Dinner'
            # get the entity value from the bot
            prediction = tracker.latest_message
            entity_value = prediction['entities'][0]['value']
            if entity_value == 'צמחוני':
                entity = "Vegetarian"
            elif entity_value == 'טבעוני':
                entity = "Vegan"
            elif entity_value == 'פלאו':
                entity = "Vegan"
            else:
                # get the alias entity from the data frame
                entity_temp = lut[lut.index == entity_value]
                entity = str(entity_temp['Entity'].values[0])
                entity2 = ""
                for i in entity:
                    if (i >= 'a' and i <= 'z') or (i >= 'A' and i <= 'Z') or i == '_':
                        entity2 += i

                if entity2[0].islower():
                    entity = entity2.capitalize()

            # get the items by ranmdom 5 of them
            items = df_noa.loc[((df_noa[entity] == 'Yes') & (df_noa[meal] == 'Yes')), ['Food_Name', entity, meal]]
            indeX = items.index.tolist()
            y = ""
            for i in range(1, 6):
                temp = random.randint(0, len(items) - 1)
                y += str(i) + ". " + str(items[items.index == indeX[temp]]['Food_Name'].values[0]) + "\n"
            dispatcher.utter_message(y)
        except:
            dispatcher.utter_message(text="אין למושג, מצטער!")


# ------------------------------------------------------------------

class ActionMealQuestion(Action):

    def name(self) -> Text:
        return "action_nutrition_meal_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        meal = []
        previous_intent = ""
        message = tracker.latest_message.get('text') if tracker.latest_message.get('text') else None
        title = 'תפריט יומי'
        # get the question from the slot
        if message is None:
            message = tracker.get_slot('x') if tracker.get_slot('x') else None
        if 'בוקר' in message:
            previous_intent = "nutrition_meal_question"
            meal = ['breakfast']
            title = 'ארוחת בוקר'
        elif 'צהריים' in message:
            previous_intent = "nutrition_meal_question"
            meal = ['lunch']
            title = 'ארוחת צהריים'
        elif 'ערב' in message:
            previous_intent = "nutrition_meal_question"
            meal = ['dinner']
            title = 'ארוחת ערב'
        else:
            meal = ['breakfast', 'lunch', 'dinner']

        try:
            res, url = core_fun(meal, title)
            dispatcher.utter_message(text="%s" % res, image=url)
        except:
            dispatcher.utter_message(text="אין למושג, מצטער!")
        return [SlotSet("x", ""), SlotSet("y", ""), SlotSet("previous_intent", previous_intent)]


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
            if ent['entity'] in lut_df[self.name()].values and ent['value'] in lut_df['Entity']:
                simple_entity = ent['value']

        try:
            feature = lut_df['Entity'][simple_entity]

            if feature in custom_df.index:
                res = custom_df.loc[feature][user_intent]
            else:
                res = custom_df[[str(s) in feature for s in custom_df.index.tolist()]][user_intent][0]

            if 'slot#' in res:
                res_list = res.split(' ')
                for k, el in enumerate(res_list):
                    if 'slot#' in el:
                        res_list[k] = tracker.get_slot(el.split('#')[1])

                res = ' '.join(res_list)

            res_list = re.findall('\{.*?\}', res)
            for match in res_list:
                res = res.replace(match, str(eval(match[1:-1])))

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

        user_intent = tracker.latest_message.get('intent').get('name')
        intent_upper = user_intent == 'nutrition_get_upper_limit'

        previous_intent = tracker.get_slot('previous_intent') if tracker.get_slot('previous_intent') else None
        if previous_intent == "nutrition_get_upper_limit" or previous_intent == "nutrition_get_rda":
            intent = previous_intent
        else:
            intent = user_intent

        rda_val, rda_units, rda_text, rda_status, nutrient = get_rda(self.name(), tracker, intent_upper)

        if rda_val > 0:

            intent_upper_str = "המקסימלית" if intent_upper else "המומלצת"
            res = "הקצובה היומית %s של %s %s היא\r %.2f %s" % \
                  (intent_upper_str, nutrient, get_personal_str(rda_status, tracker), rda_val, rda_units)

            res += "\r"
            res += rda_text if rda_text else ""

        else:

            if rda_text:
                res = rda_text
            else:
                res = "אין לי מושג, מצטער!"

        dispatcher.utter_message(text="%s" % res)

        return [SlotSet("previous_intent", intent), SlotSet("x", ""), SlotSet("y", "")]


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
        user_intent = tracker.latest_message.get('intent').get('name')
        intent_upper = user_intent == 'nutrition_get_upper_limit'

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

        regex_res = re.search('כמה (.*) יש ב(.*)', user_msg.replace('?', ''))
        if regex_res:
            x = regex_res.group(1)
            y = regex_res.group(2).strip()

        if not y:
            regex_res = re.search('.* ב(.*)', user_msg.replace('?', ''))
            if regex_res:
                y = regex_res.group(1).strip()

        food_units = "100 גרם"
        regex_units_res = re.search('(.*) של (.*)', y) if y else None
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

            food = db_df[db_df['shmmitzrach'].str.contains(y_common)].iloc[0, :]
            feature = lut_df[lut_df.index == x]["Entity"][0]
            units = lut_df[lut_df.index == x]["Units"][0]

            food_units_row = pd.Series()
            if food_units:
                food_units_row = units_df[(units_df['smlmitzrach'] == int(food['smlmitzrach'])) &
                                          (units_df['shmmida'] == food_units)]

            is_food_units_match = not food_units_row.empty or food_units == "100 גרם"

            food_units_factor = 1.0
            if not food_units_row.empty:
                food_units_factor = food_units_row['mishkal'].values[0] / 100

            val = food[feature] * food_units_factor

            # calculating the cake diagram feature
            # 1 gram fat is 9 calories
            # 1 gram protein is 4 calories
            # 1 gram carb is 4 calories
            fat_calories = int(food['total_fat'] * food_units_factor * 9)
            protein_calories = int(food['protein'] * food_units_factor * 4)
            carbs_calories = int(food['carbohydrates'] * food_units_factor * 4)
            title = "ב" + y_common
            data = {'שומן': fat_calories,
                    'פחמימות': carbs_calories,
                    'חלבונים': protein_calories}
            url = iniliatize_Diagram(title, data)

            if units == 0:
                res = "ב-%s של %s יש %.2f %s" % (food_units, food['shmmitzrach'], float(val), x)
            else:
                res = ""
                if not is_food_units_match:
                    res = "לא הצלחתי למצוא נתונים במאגר על היחידה %s עליה שאלת\r" % food_units
                    res += "היחידות הבאות קיימות במאגר, עבור %s:\r" % food['shmmitzrach']
                    res += ', '.join(
                        units_df[units_df['smlmitzrach'] == int(food['smlmitzrach'])]['shmmida'].to_list())
                    res += "\r"
                    food_units = "100 גרם"

                res += "ב-%s של %s יש %.2f %s %s" % (food_units, food['shmmitzrach'], float(val), units, x)

            rda_val, rda_units, rda_text, rda_status, nutrient = get_rda(name_xy, tracker, intent_upper)

            if rda_val > 0 and units not in ['יחב"ל']:
                rda = 100 * float(val) / rda_val
                intent_upper_str = "המקסימלית" if intent_upper else "המומלצת"
                res += "\r"
                res += "שהם כ-%d אחוז מהקצובה היומית %s %s" % (
                    int(rda), intent_upper_str, get_personal_str(rda_status, tracker))

            res += "\r"
            res += rda_text if rda_text else ""

            dispatcher.utter_message(text="%s" % res, image=url)

        except:
            dispatcher.utter_message(text="אין לי מושג כמה, מצטער!")

        return [SlotSet("x", x), SlotSet("y", y), SlotSet("previous_intent", "nutrition_howmanyxiny")]


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
        food = ""
        food_entity = ""
        x = tracker.get_slot('x') if tracker.get_slot('x') else None
        if x is not None and x is not "":
            food = x
            food_entity = x
        else:
            for ent in tracker.latest_message.get('entities'):
                if ent['entity'] in lut_df[self.name()].values:
                    food_entity = ent['value']
                    food = food_entity
                    break

        try:

            if food in common_df.index:
                food = common_df[common_df.index == food]['shmmitzrach'][0]

            food = db_df[db_df['shmmitzrach'].str.contains(food)].iloc[0, :]

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

        return [SlotSet("previous_intent", "nutrition_is_food_healthy"), SlotSet("x", ""), SlotSet("y", "")]


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
            regex_res = re.search('.* או (.*)', user_msg.replace('?', ''))
            if regex_res:
                food_entity2 = regex_res.group(1).strip()

        try:

            nutrition_density_cmp = []
            advantages_cmp = []
            disadvantages_cmp = []

            for food_entity in (food_entity1, food_entity2):

                food = food_entity

                if food in common_df.index:
                    food = common_df[common_df.index == food]['shmmitzrach'][0]

                food = db_df[db_df['shmmitzrach'].str.contains(food)].iloc[0, :]

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
                res = "לפי צפיפות תזונתית %s עדיף על פני %s\r" % (food_entity1, food_entity2)
            elif nutrition_density_cmp[0] < nutrition_density_cmp[1]:
                res = "לפי צפיפות תזונתית %s עדיף על פני %s\r" % (food_entity2, food_entity1)
            else:
                res = "לפי צפיפות תזונתית %s ו-%s שקולים\r" % (food_entity1, food_entity2)

            if nutrition_density_cmp[0] < nutrition_density_cmp[1]:
                advantages_cmp.reverse()
                disadvantages_cmp.reverse()

            for advantage in advantages_cmp:
                if advantage:
                    res += "%s\r" % advantage

            for disadvantage in disadvantages_cmp:
                if disadvantage:
                    res += "%s\r" % disadvantage

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

            food = db_df[db_df['shmmitzrach'].str.contains(food)].iloc[0, :]

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
                                         ((bloodtest_df['Gender'] == "ANY") | (
                                                 bloodtest_df['Gender'] == gender_str)) & \
                                         ((bloodtest_df['Age min'] == "ANY") | (
                                                 bloodtest_df['Age min'].replace('ANY', -1).astype(float) <= age)) & \
                                         ((bloodtest_df['Age Max'] == "ANY") | (
                                                 bloodtest_df['Age Max'].replace('ANY', -1).astype(float) > age))]

            bloodtest_type = bloodtest_row['Graph type'].values[0]
            bloodtest_min = bloodtest_row['Min'].values[0]
            bloodtest_thr1 = bloodtest_row['Threshold 1'].values[0]
            bloodtest_thr2 = bloodtest_row['Threshold 2'].values[0]
            bloodtest_max = bloodtest_row['Max'].values[0]

            if bloodtest_type == 1:
                res = 'ערך תקין עבור בדיקת %s בין %.2f ועד %.2f, ערך מעל %.2f נחשב חריג' % (
                    bloodtest_entity, bloodtest_min, bloodtest_thr1, bloodtest_thr2)

            elif bloodtest_type == 2:
                res = 'ערך תקין עבור בדיקת %s בין %.2f ועד %.2f, ערך מתחת %.2f נחשב חריג' % (
                    bloodtest_entity, bloodtest_thr2, bloodtest_max, bloodtest_thr1)

            elif bloodtest_type == 3:
                res = 'ערך תקין עבור בדיקת %s בין %.2f ועד %.2f' % (
                    bloodtest_entity, bloodtest_thr1, bloodtest_thr2)

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
            regex_res = re.search('האם (.*) הוא .*', user_msg.replace('?', ''))
            if regex_res:
                val = regex_res.group(1).strip()

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
                                         ((bloodtest_df['Gender'] == "ANY") | (
                                                 bloodtest_df['Gender'] == gender_str)) & \
                                         ((bloodtest_df['Age min'] == "ANY") | (
                                                 bloodtest_df['Age min'].replace('ANY', -1).astype(float) <= age)) & \
                                         ((bloodtest_df['Age Max'] == "ANY") | (
                                                 bloodtest_df['Age Max'].replace('ANY', -1).astype(float) > age))]

            bloodtest_type = bloodtest_row['Graph type'].values[0]
            bloodtest_min = bloodtest_row['Min'].values[0]
            bloodtest_thr1 = bloodtest_row['Threshold 1'].values[0]
            bloodtest_thr2 = bloodtest_row['Threshold 2'].values[0]
            bloodtest_max = bloodtest_row['Max'].values[0]

            if bloodtest_type == 1:
                if bloodtest_min <= float(val) <= bloodtest_thr1:
                    res = 'כן, זהו ערך תקין עבור בדיקת %s היות והוא נופל בטווח בין %.2f ועד %.2f. ערך מעל %.2f נחשב לחריג' % (
                        bloodtest_entity, bloodtest_min, bloodtest_thr1, bloodtest_thr2)
                else:
                    res = 'לא, זהו אינו ערך תקין עבור בדיקת %s. ערך תקין הינו בטווח בין %.2f ועד %.2f. ערך מעל %.2f נחשב לחריג' % (
                        bloodtest_entity, bloodtest_min, bloodtest_thr1, bloodtest_thr2)

            elif bloodtest_type == 2:
                if bloodtest_thr2 <= float(val) <= bloodtest_max:
                    res = 'כן, זהו ערך תקין עבור בדיקת %s היות והוא נופל בטווח בין %.2f ועד %.2f. ערך מתחת %.2f נחשב לחריג' % (
                        bloodtest_entity, bloodtest_thr2, bloodtest_max, bloodtest_thr1)
                else:
                    res = 'לא, זהו אינו ערך תקין עבור בדיקת %s. ערך תקין הינו בטווח בין %.2f ועד %.2f. ערך מתחת %.2f נחשב לחריג' % (
                        bloodtest_entity, bloodtest_thr2, bloodtest_max, bloodtest_thr1)

            elif bloodtest_type == 3:
                if bloodtest_thr1 <= float(val) <= bloodtest_thr2:
                    res = 'כן, זהו ערך תקין עבור בדיקת %s היות והוא נופל בטווח בין %.2f ועד %.2f' % (
                        bloodtest_entity, bloodtest_thr1, bloodtest_thr2)
                else:
                    res = 'לא, זהו אינו ערך תקין עבור בדיקת %s. ערך תקין הינו בטווח בין %.2f ועד %.2f.' % (
                        bloodtest_entity, bloodtest_thr1, bloodtest_thr2)

            else:
                raise Exception()

            dispatcher.utter_message(text="%s" % res)

        except:
            dispatcher.utter_message(text="אין לי מושג, מצטער!")

        return []


# ------------------------------------------------------------------

class ActionFoodSubstituteQuestion(Action):

    def name(self) -> Text:
        return "action_nutrition_food_substitute"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        db_dict = load_db(0xc33)

        db_df = db_dict['tzameret']
        lut_df = db_dict['lut']
        features_df = db_dict['food_units_features']
        common_df = db_dict['common_food']
        food_ranges_df = db_dict['food_ranges']
        subs_tags_alias_df = db_dict['subs_tags_alias']

        user_msg = tracker.latest_message.get('text')

        for ent in tracker.latest_message.get('entities'):
            if ent['entity'] in lut_df[self.name()].values:
                food_entity = ent['value']
                break

        tzameret_groups_lut = {}
        tzameret_groups_lut['1'] = ['1', '4']  # Milk
        tzameret_groups_lut['2'] = ['1', '2', '3', '4']  # Meat
        tzameret_groups_lut['3'] = ['1', '2', '3', '4']  # Eggs
        tzameret_groups_lut['4'] = ['1', '4']  # Dairy
        tzameret_groups_lut['5'] = ['5', '6', '7', '9']  # Snacks
        tzameret_groups_lut['6'] = ['5', '6', '7', '9']  # Fruits
        tzameret_groups_lut['7'] = ['5', '6', '7', '9']  # Vegetables
        tzameret_groups_lut['8'] = ['8', '4']  # Fat
        tzameret_groups_lut['9'] = ['5', '6', '7', '9']  # Beverages

        food_energy_thr = 0.05

        def get_advantages(food):
            advantages = []
            for idx, row in food_ranges_df.iterrows():
                if row["tzameret_name"] and row["tzameret_name"] in food:
                    if row["good_or_bad"] == "good":
                        value = float(food[row["tzameret_name"]])
                        if idx == "Protein":
                            threshold = 250
                        else:
                            threshold = float(row["Medium - threshold per 100gr"])
                        if value > threshold:
                            advantages.append(row["hebrew_name"])
            return advantages

        def get_advantages_score(food):
            act = food['advantages']
            ref = ast.literal_eval(food['advantages_ref'])
            intersection = []
            if isinstance(act, list) and isinstance(ref, list):
                intersection = list(set(act) & set(ref))
            return len(intersection)

        try:

            food = food_entity
            if food in common_df.index:
                food = common_df[common_df.index == food]['shmmitzrach'][0]

            food_tzameret = db_df[db_df['shmmitzrach'].str.contains(food)].iloc[0, :]
            tzameret_code = int(food_tzameret['smlmitzrach'])
            tzameret_code_msb = food_tzameret['smlmitzrach'][0]
            food_energy = food_tzameret['food_energy']
            food_features = features_df[features_df['smlmitzrach'].fillna(0).astype(int) == tzameret_code]

            user_msg_feature_v = []
            user_msg_feature_k = list(
                set(subs_tags_alias_df.index.to_list()) & set(user_msg.replace(',', '').split(" ")))
            for tag in user_msg_feature_k:
                tag_df = subs_tags_alias_df[subs_tags_alias_df.index == tag]['Entity']
                if tag_df.any:
                    user_msg_feature_v.append(tag_df.values[0])

            food_filter_1 = db_df[db_df['smlmitzrach'].str[0].isin(tzameret_groups_lut[tzameret_code_msb])]
            food_filter_2 = db_df[abs(db_df['food_energy'] - food_energy) / food_energy < food_energy_thr]
            food_filter_1_2 = pd.merge(food_filter_1, food_filter_2, how='inner')
            food_filter_1_2['smlmitzrach'] = food_filter_1_2['smlmitzrach'].astype(float)
            food_filter = features_df[features_df['smlmitzrach'].isin(food_filter_1_2['smlmitzrach'].to_list())]
            food_filter = food_filter[~food_filter['Food_Name'].str.contains(food_entity)]
            for tag in user_msg_feature_v:
                food_filter = food_filter[food_filter[tag] == 'Yes']
            food_filter = food_filter.reset_index(drop=True)

            if food_features.empty:
                food_filter['features_score'] = 0
            else:
                food_features_compact = food_features.iloc[:, 5:-4]
                food_filter_compact = food_filter.iloc[:, 5:-4].reset_index(drop=True)

                food_features_compact_shaped = pd.DataFrame(
                    np.repeat(food_features_compact.values, len(food_filter_compact), axis=0))
                food_features_compact_shaped.reset_index(drop=True)
                food_features_compact_shaped.columns = food_features_compact.columns

                food_features_score_df = (food_filter_compact == food_features_compact_shaped).astype(int)
                food_filter['features_score'] = food_features_score_df.sum(axis=1)

            food_advantages = get_advantages(food_tzameret)
            food_filter['advantages'] = food_filter_1_2.apply(get_advantages, axis=1)
            food_filter['advantages_ref'] = str(food_advantages)
            food_filter['advantages_score'] = food_filter.apply(get_advantages_score, axis=1)

            food_filter = food_filter.sort_values(['features_score', 'advantages_score'], ascending=False)

            res = "להלן 5 התחליפים הקרובים ביותר עבור %s" % food_entity
            res += "\n"
            res += '\n'.join(list(food_filter['Food_Name'].values[:5]))

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

class ProfileFormValidator(FormValidationAction):
    """ProfileForm Validator"""

    def name(self) -> Text:
        return "validate_profile_form"

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Optional[List[Text]]:
        required_slots = ["phone", "username", "gender", "age", "weight", "height"]

        return required_slots

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
            phone_value = value.replace('-', '').replace(' ', '')

            pkl_db = './persons.pkl'
            if path.exists(pkl_db):
                df = pd.read_pickle(pkl_db)
                if phone_value in df.index:
                    dispatcher.utter_message(
                        text="פרטיך נטענו בהצלחה, ברוכים השבים %s" % df.loc[phone_value].username)
                    return {'phone': phone_value,
                            'username': df.loc[phone_value].username,
                            'gender': df.loc[phone_value].gender,
                            'age': df.loc[phone_value].age,
                            'weight': df.loc[phone_value].weight,
                            'height': df.loc[phone_value].height}
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
