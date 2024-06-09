import initialCleaner
import pandas as pd
import os
import datetime
import ast
import random
import csv
from dateutil.relativedelta import relativedelta
import math


def degree_applyer(row):
    """
    Assigning boolean value of user's educational status based on:
        1. Current occupation as student,
        2. University name.
    Output:    
        True - user has higher degree,
        False - user has not higher degree.
    """
    if row['university'] != 'none':
        return True
    elif row['occupation'] == 'university':
        return True
    elif row['university'] == 'none' and row['occupation'] in ['none', 'work', 'school']:
        return False
    else:
        raise ValueError(f'Error in degree_applyer ----- unknown value ----- {row}')


def career_applyer(row):
    """
    Assigning boolean value of user's work status based on:
        1. Current occupation as work,
        2. Career position.
    Output:    
        True - user employed,
        False - user unemployed.
    """
    if row['career'] != 'none':
        return True
    if row['occupation'] == 'work':
        return True
    else:
        return False


def city_map_writer(uniques):
    """ Writes city map to file for further decoding. """
    cities_list = uniques.to_list()
    with open('city_map.csv', 'w', encoding="UTF-8") as file:
        writer = csv.writer(file)
        for index, city in enumerate(cities_list):
            writer.writerow([index, city])

 
def age_extractor(bdate):
    age = relativedelta(datetime.datetime.today(), bdate).years
    if age > 90:
        return 0
    elif age < 10:
        return 0
    else:
        return age


def age_categorizer(age):
    """
    Assigning the category based on user's age:
        0 - unknown age category,
        1 - teenager,
        2 - young person,
        3 - middle aged person,
        4 - old person.
    """
    if age == 0:
        return 0
    if age >= 10 and age <= 20:
        return 1
    if age >= 21 and age <= 40:
        return 2
    if age >= 41 and age <= 60:
        return 3
    if age >= 61 and age < 90:
        return 4


def opposition_support_ratio(group_type_list):
    """
    Сounting the support ratio and normilizing it by dividing to maximum number of groups with that exact type:
        0 — 100% government support,
        0.5 — indifferent or unknown support,
        1 — 100% opposition support.
    
    Scaling factor used to increase dispersion for better AI training.
        
    Hack:
    In this function we use hardcoded maximum number of groups each type.
    We can count them dynamically, but this is redundant in our case.
    We are have limited number of groups, all of which was marked manually, so we will also keep the total number manually entered.
    Initial markering can be found in VkDataCollector/group_list.csv:
    1 - for government group, 2 - for opposition group.
    Then we stored it in group_type string in each row, and then processsed it and converted to list in handle_duplicates function.
    """
    ratio_group1 = group_type_list.count(1) / 20 # 20 - maximum number of government groups (hardcoded).
    ratio_group2 = group_type_list.count(2) / 22 # 22 - maximum number of opposition groups (hardcoded).
    total_ratio = ratio_group2 - ratio_group1
    scale_factor = 0.1 # Factor for increasing dispersion. Can be edited.
    if total_ratio < 0:
        opposition_ratio = - math.pow((- total_ratio), scale_factor)
    else:
        opposition_ratio = math.pow(total_ratio, scale_factor)
    opposition_ratio = (opposition_ratio + 1) / 2
    return opposition_ratio


def friends_cleaner(friends_list, users_id_set):
    """
    Keep friends that are only present in initial dataset and reduce them to maximum of 20.
    Input: set of all VK id's that are present in initial dataset.
    Output: list of friends ids.
    """
    friends_list = ast.literal_eval(friends_list) # Converting string to the actual list.
    updated_list = []
    for friend_id in friends_list:
        if friend_id in users_id_set:
            updated_list.append(friend_id)
    if len(updated_list) > 20:
        updated_list = random.sample(updated_list, 20)
    return updated_list


def friends_data_loader(df, sampled_df):
    """
    Creates new dataframe with flat data structure.
    
    Our goal is to iterate through all friends in each row and append friend's parameters to corresponding column.
        Example: [id, last_seen_platofrm, ... , friend1-id, friend1-last_seen_time, ...]
    
    Outputs:
        New dataframe with flat structure.
    """
    initial_columns = ['id', 'last_seen_platform', 'political', 'sex', 'higher_degree', 'employment', 'city_code', 'age', 'age_category', 'opposition_support_ratio']
    new_df = pd.DataFrame(columns=initial_columns) # Creating blank dataframe.

    def row_updater(row):
        new_df.loc[-1] = row # Adding existing data from the current row to dataframe.
        for index, friend_id in enumerate(row['friends_ids']):
            found_row = df[df['id'] == friend_id].copy() # Finding row with friend_id in initial dataframe.
            found_row.drop(columns='friends_ids', inplace=True)
            # Appending friends data to the resulting dataframe.
            # TODO: Probably poor perfomance. Cosider rewriting this block.
            new_df.at[-1, f'friend{index}-id'] = found_row['id'].iloc[0] # TODO: Remove ids after debug.
            new_df.at[-1, f'friend{index}-last_seen_platform'] = found_row['last_seen_platform'].iloc[0]
            new_df.at[-1, f'friend{index}-political'] = found_row['political'].iloc[0]
            new_df.at[-1, f'friend{index}-sex'] = found_row['sex'].iloc[0]
            new_df.at[-1, f'friend{index}-higher_degree'] = found_row['higher_degree'].iloc[0]
            new_df.at[-1, f'friend{index}-employment'] = found_row['employment'].iloc[0]
            new_df.at[-1, f'friend{index}-city_code'] = found_row['city_code'].iloc[0]
            new_df.at[-1, f'friend{index}-age'] = found_row['age'].iloc[0]
            new_df.at[-1, f'friend{index}-age_category'] = found_row['age_category'].iloc[0]
            new_df.at[-1, f'friend{index}-opposition_support_ratio'] = found_row['opposition_support_ratio'].iloc[0]
        new_df.index = new_df.index + 1
    
    for _, row in sampled_df.iterrows():
        if row['friends_ids'] == []:
            new_df.loc[-1] = row
            new_df.index = new_df.index + 1
            continue
        row_updater(row)
    return new_df


def main():
    # initialCleaner.main()
    os.chdir('datasets')
    df = pd.read_parquet('dataset.parquet')
    print('initial dataset loaded')
    
    # Basic data preparing for whole loaded dataset
    df.drop(columns=['friends_count', 'langs', 'verified'], inplace=True)
    df['higher_degree'] = df.apply(degree_applyer, axis=1) # Setting True/False for higher degree
    df['employment'] = df.apply(career_applyer, axis=1) # Setting True/False for employment status
    df['city_code'], uniques = pd.factorize(df['city'])
    city_map_writer(uniques)
    df['age'] = df['bdate'].apply(age_extractor)
    df['age_category'] = df['age'].apply(age_categorizer)
    df['group_type'] = df['group_type'].apply(lambda x: ast.literal_eval(x.decode('UTF-8'))) # Fixing group_type value format after initial parquet import
    df['opposition_support_ratio'] = df['group_type'].apply(opposition_support_ratio)
    df.drop(columns=['occupation', 'career', 'university', 'bdate', 'city', 'group_type', 'connection_type'], inplace=True)
    print('basic data preparation done')
    
    # Reducing our dataset to 10.000 random value and cutting friends based on presence in our dataset
    sampled_df = df.sample(n=10000)
    users_id_set = set(df['id']) # Loading all id's to memory for fast access
    sampled_df['friends_ids'] = sampled_df['friends_ids'].apply(lambda x: friends_cleaner(x, users_id_set))
    users_id_set = None # Releasing memory
    print('Start flatting data')
    flat_df = friends_data_loader(df, sampled_df)
    print('Finish flatting data')
    flat_df.to_csv('10Kflat.csv', index=False)
    flat_df.to_parquet('10Kflat.parquet', index=False)

if __name__ == "__main__":
    main()