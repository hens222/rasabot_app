import numpy as np
import pandas as pd



# Dictionary that is equivalent to user inputs and filters the df_noa Database based on the inputs

types = []

dic = {'breakfast': 'ארוחת בוקר', 'lunch': 'ארוחת צהריים', 'dinner': 'ארוחת ערב'}


def arrayToString(s):
    str1 = ""

    for ele in s:
        str1 += str(ele)
    return str1.replace(',', '')


def update_budgets(daily_budget, meals_num, snacks_num, weights):
    """Takes total budget, number of meals and snacks, and weights as paramters. Returns budget for each category for
    every meal """
    # change 0.3 to a user params
    budgets = {}
    div = (meals_num + inputs.get(
        'budget_var') * snacks_num)  # Is this supposed to be budget_var(0.3) times snacks num or budget_var times meals_num
    if div > 0:
        budgets['meal'] = round(daily_budget / div, 1)
        budgets['snack'] = round(inputs.get('budget_var') * daily_budget, 1)

        budgets['Carbs'] = round(weights[0] * budgets['meal'], 1)
        budgets['Protein'] = round(weights[1] * budgets['meal'], 1)
        budgets['Vegetables'] = round(weights[2] * budgets['meal'], 1)
        budgets['Fruits'] = round(weights[3] * budgets['snack'], 1)
        budgets['Fat'] = round(weights[4] * budgets['snack'], 1)
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
    return total


def update_calorie_budgets(candidate_calories, item_type, bud):
    '''Updates the calories budget based on how many calories were already used'''

    bud[item_type] = bud[item_type] - candidate_calories
    return bud


def build_meal(meals_bank, meal_type, budget):
    '''Builds a meal taking a DataFrame, meal type and budget as parameters. Meal takes item from each category (Carbs, Protein etc.) and returns the meal, weighted average score and total meal calories'''
    budget_weights = {**budget_weights_meals, **budget_weights_snacks_fruits_fat, **budget_weights_savoury_snacks,
                      **budget_weights_sweets}
    bud = {}
    max_meal_items = inputs.get('max_items')
    meal_score = 0
    score_list = []
    uti_score = []
    ind_score = []
    meals = []
    meal_cals = 0

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
                types.append(df['food_category'])
            candidate_units = candidate_units_amounts(df, int(df['primary_sn'].values[0]), item_type)
            candidate_grams = candidate_units[0]
            for can_grams in candidate_grams:
                sn = float(df['primary_sn'].values[0])
                for candidate_amount in candidate_units[1]:
                    for amount in reversed(candidate_amount):
                        calories = get_item_property(sn, can_grams, amount)
                        can_cals = getattr(calories, "tolist", lambda: candidate_calories)()
                        if can_cals < budget[item_type]:
                            success = True
                            if success:
                                sn1 = float(df['primary_sn'].values[0])
                                calories1 = get_item_property(sn1, can_grams, amount)
                                bud[item_type] = getattr(calories1, "tolist", lambda: candidate_calories)()
                                units_priority = candidate_grams.index(can_grams) + 1
                                meal_score += 1 / units_priority
                                item_score = (bud[item_type]) / (budget[item_type])
                                df['score'] = item_score
                                score_list.append(item_score)
                                dataframe = df[['food_name', 'primary_sn']]
                                meals.append(dataframe)
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
    if len(ind_score) < len(item_types[meal_type]):
        ind_score.append(0.000001)
        uti_score.append(.35)
    if (min(ind_score) < 0.7) and (meal_type != 'snack'):
        extra_penalty = inputs.get('extra_penalty')
    else:
        extra_penalty = 0
    total_utilization = sum(x * y for x, y in zip(ind_score, uti_score)) / sum(uti_score)
    penalty_score = 1 - meal_score / len(meals)
    score = total_utilization - (penalty_score * inputs.get('penalty_weight')) - extra_penalty

    return meals, score, meal_cals


def build_meal_wrapper():
    # Builds and populates a scoreboard that sorts the meals based on their score
    x = -3

    pd.set_option('precision', 2)
    budget_weights = {**budget_weights_meals, **budget_weights_snacks_fruits_fat, **budget_weights_savoury_snacks,
                      **budget_weights_sweets}
    budget_weights_list = []
    for k, v in budget_weights.items():
        budget_weights_list.append(v)

    score_tracker = -2
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
            meal_budget = update_budgets(inputs.get('total_cals'), inputs.get('meals_num'), inputs.get('snacks_num'),
                                         budget_weights_list)
            if meal_type != 'snack':
                mealy, scorey, calsy = build_meal(bank, meal_type, budgets_dynamic)
                if mealy:
                    scoreboard[meal_type] = mealy, scorey, calsy
                    if scoreboard[meal_type][1] > score_tracker:
                        score_tracker = scoreboard[meal_type][1]
                        total_cals = scoreboard[meal_type][2]
            else:
                mealx, scorex, calsx = build_meal(bank, meal_type, meal_budget)

                if mealx:
                    scoreboard[meal_type] = mealx, scorex, calsx

            if scoreboard:
                meals[meal_type] = scoreboard[meal_type]

            for meal_name, whole_meal in scoreboard.items():
                df = pd.concat(whole_meal[0])
                df = pd.DataFrame(df.values.reshape(1, -1))
                df['score'] = float(scoreboard[meal_type][1])
                df['meal_cals'] = scoreboard[meal_type][2]
                if meal_name != 'snack':
                    df['meal_name'] = meal_name
                    df['budget per meal'] = meal_budget.get('meal')
                    df['meal budget utilization'] = (df['meal_cals'] / df['budget per meal'])
                    # df['meal budget utilization'] = ((df['meal_cals']/df['budget per meal']) * 100).astype(str) + '%'
                else:
                    df['meal_name'] = meal_name
                    df['budget per snack'] = budgets_dynamic.get('snack')
                    df['snack budget utilization'] = (df['meal_cals'] / df['budget per snack']) * 100
                df.set_index('meal_name', drop=True, inplace=True)
                filler.append(df)
                if meal_name != 'snack':
                    # rename all the budget as budget leftover so its carbs budget leftover etc.
                    df['carb budget per meal'] = float(format(meal_budget.get('Carbs'), '.2f'))
                    df['carbs budget remaining'] = float(format(budgets_dynamic.get('Carbs'), ".2f"))
                    df['carb budget utilization'] = float(
                        format((meal_budget.get('Carbs') - budgets_dynamic.get('Carbs')) / meal_budget.get('Carbs'),
                               '.2f'))
                    df['protein budget per meal'] = float(format(meal_budget.get('Protein'), '.2f'))
                    df['protein budget remaining'] = float(format(budgets_dynamic.get('Protein'), '.2f'))
                    df['protein budget utilization'] = float(format(
                        (meal_budget.get('Protein') - budgets_dynamic.get('Protein')) / meal_budget.get('Protein'),
                        '.2f'))
                    df['vegetable budget per meal'] = float(format(meal_budget.get('Vegetables'), '.2f'))
                    df['vegetable budget remaining'] = float(format(budgets_dynamic.get('Vegetables'), '.2f'))
                    df['vegetable budget utilization'] = float(format(
                        (meal_budget.get('Vegetables') - budgets_dynamic.get('Vegetables')) / meal_budget.get(
                            'Vegetables'), '.2f'))
                else:
                    if snacks.get('sweets') == "Yes":
                        df['sweets budget per snack'] = float(format(budgets_dynamic.get('Sweets'), '.2f'))
                        df['sweets budget remaining'] = float(format(meal_budget.get('Sweets'), '.2f'))
                        df['sweets budget utilization'] = float(format(
                            (budgets_dynamic.get('Sweets') - meal_budget.get('Sweets')) / budgets_dynamic.get('Sweets'),
                            '.2f'))
                    if snacks.get('Savoury_Snacks') == 'Yes':
                        df['savoury budget per snack'] = float(format(budgets_dynamic.get('Savoury_Snacks'), '.2f'))
                        df['savoury budget remaining'] = float(format(meal_budget.get('Savoury_Snacks'), '.2f'))
                        df['savoury budget utilization'] = float(format((budgets_dynamic.get(
                            'Savoury_Snacks') - meal_budget.get('Savoury_Snacks')) / budgets_dynamic.get(
                            'Savoury_Snacks'), '.2f'))
                    if user_params.get('fruits') == 'No':
                        df['fruits budget per snack'] = float(format(budgets_dynamic.get('Fruits'), '.2f'))
                        df['fruits budget remaining'] = float(format(meal_budget.get('Fruits'), '.2f'))
                        df['fruits budget utilization'] = float(format(
                            (budgets_dynamic.get('Fruits') - meal_budget.get('Fruits')) / budgets_dynamic.get('Fruits'),
                            '.2f'))
                    df['fat budget per snack'] = float(format(budgets_dynamic.get('Fat'), '.2f'))
                    df['fat budget remaining'] = float(format(meal_budget.get('Fat'), '.2f'))
                    df['fat budget utilization'] = float(
                        format((budgets_dynamic.get('Fat') - meal_budget.get('Fat')) / budgets_dynamic.get('Fat'),
                               '.2f'))

        if meal_type == 'snack':
            user_snacks_num -= 1
        else:
            user_meals_num -= 1

    df_meals = pd.concat(filler)
    df_final = df_meals.sort_values(by=['meal_name', 'score'], ascending=[True, False])
    x = 1
    y = 1
    for b in range(0, inputs.get('max_items') * 2, 2):
        df_final.rename(columns={b: ('Item ' + str(x))}, inplace=True)
        x = x + 1
    for m in range(1, inputs.get('max_items') * 2, 2):
        df_final.rename(columns={m: ('Primary SN ' + str(y))}, inplace=True)
        df_final.fillna(0, inplace=True)
        df_final[('Primary SN ' + str(y))] = df_final[('Primary SN ' + str(y))].apply(int)
        y = y + 1

    return df_final


def displayMeal(data, mealType):
    menu = ""
    calories = 0
    # hole day menu
    if len(mealType) > 1:
        for meal in mealType:
            items, temp_calories = getMeal(data, meal)
            calories += temp_calories
            menu = menu + items
    # one meal for the user
    else:
        menu, calories = getMeal(data, mealType[0])
    menu = menu + "כמות קלוריות -> " + arrayToString(str(calories))
    return menu


def getMeal(data, meal_type):
    temp_meal = data[data.index == meal_type]
    first, second, third = temp_meal['Item 1'].head(1).values, temp_meal['Item 2'].head(1).values, temp_meal[
        'Item 3'].head(
        1).values
    calories = temp_meal['meal_cals'].head(1).values
    return dic[meal_type]+":\n1. " + arrayToString(first) + "\n2. " + arrayToString(second) + "\n3. " + arrayToString(third) + "\n", int(calories)


def Core_fun(meal_type, sheets):
    global snacks, user_params, units_thr, type_thr, budget_weights_meals, budget_weights_snacks_fruits_fat, budget_weights_savoury_snacks, budget_weights_sweets, inputs, display_user_parameter, debug

    global user_meals_num, total_cals, user_snacks_num, candidate_calories, types

    global df_noa, df_tzameret_food_group, df_weights, df_nutrition

    #get the sheets from the actions
    df_noa,df_tzameret_food_group,df_weights,df_nutrition = sheets

    user_params = {'eggs': 'No',  # If eggs = Yes, filters out all the meals with eggs
                   'vegetables': 'No',  # If vegetables = Yes, fiters out all meals with vegetables
                   'fruits': 'No',
                   # If fruits = Yes, filters out all snacks and meals with fruits and snacks don't have fruits as a category
                   'dairy': 'No',  # If dairy = Yes, filters out all the dairy items
                   'beef_chicken_fish': 'No',
                   # If beef_chicken_fish = Yes, filters out all the meals with beef chicken or fish
                   # For remaining if Yes, filters only the food its for (i.e if kosher = Yes, only shows kosher food)
                   'kosher': 'yes',
                   'halal': 'No',
                   'vegetarian': 'No',
                   'vegan': 'No',
                   'ketogenic': 'Yes',
                   'paleo': 'No',
                   'mediterranean': 'Yes',
                   'lactose_free': 'No',
                   'gluten_free': 'No',
                   'milk_free': 'No',
                   'wheat_free': 'No',
                   'egg_free': 'yes',
                   'soy_free': 'No',
                   'tree_nut_free': 'No',
                   'peanut_free': 'No',
                   'fish_free': 'No',
                   'shellfish_free': 'No'}
    # Dictionary to see if want to add certain snack elements to the snacks on the scoreboard
    snacks = {'sweets': 'Yes',
              'Savoury_Snacks': 'Yes'}

    # Threshold for the build meal to stop looking for another item (If there are only 20 Carb calories left the meal exits the Carb code and moves to Protein):
    units_thr = {'Carbs': 10,
                 'Protein': 12,
                 'Vegetables': 15,
                 'Fat': 30,
                 'Fruits': 25,
                 'Sweets': 25,
                 'Savoury_Snacks': 25}

    # Another threshold for build meal to stop looking for another item in the category if there is less budget than
    # the threshold:
    type_thr = {'Carbs': 25,
                'Protein': 10,
                'Vegetables': 10,
                'Fat': 25,
                'Fruits': 10,
                'Sweets': 25,
                'Savoury_Snacks': 25}

    # For snacks its either fruits and fat or savoury or sweets
    budget_weights_meals = {'Carbs': 0.15,
                            'Protein': 0.60,
                            'Vegetables': 0.45}

    budget_weights_snacks_fruits_fat = {'Fruits': 0.75,
                                        'Fat': 0.35}

    budget_weights_savoury_snacks = {'Savoury_Snacks': 1.05}

    budget_weights_sweets = {'Sweets': 1.05}

    # User inputs that control different variables:
    inputs = {'budget_var': 0.3,  # Budget variable to see the weighting for snacks and individual meals
              'item_thr': 4,  # Threshold used to decided when to break code if there is less than 5 total budget left
              'max_items': 3,  # Max amount of items per meal
              'penalty_weight': 1,
              # Penalty weight for the meal score if the meal doesnt take the first option at the intersection of
              # mida max amount meal
              'max_iter': 7,  # Number of meals for each meal type in the scoreboard
              'meals_num': 3,  # Number of different meal types and meals - will always be 3
              'snacks_num': 2,  # number of snacks in the final scoreboard
              'extra_penalty': 0.2,  # Penalty if there is less than 0.7 of each categroy for the budget is used
              'total_cals': 2000}  # total calories in the budget for the day

    debug = {'debug_en': True}  # Used for finding bugs in code. Set to True for code to run properly
    # Toggle to show the user values in a DataFrame

    meals2 = build_meal_wrapper()

    items = displayMeal(meals2, meal_type)
    return items



