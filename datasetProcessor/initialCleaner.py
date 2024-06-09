import pandas as pd
import os
import glob
import json

def combine_files():
  os.chdir('datasets')
  path = 'datasets_row'
  files = glob.glob(os.path.join(path , "*.csv"))
  li = []
  print(path)

  for file in files:
    print(file)
    frame = pd.read_csv(file)
    li.append(frame)

  df = pd.concat(li, ignore_index=True)
  return df


def remove_closed_accounts(df):
  df.drop(df[df.is_closed == True].index, inplace=True)
  df.drop(df[df.verified.isnull()].index, inplace=True)
  if (df[df.is_closed == True].index).empty:
    print('Closed accounts was removed')
  else:
    print('Error: Closed accounts was not removed!!!')
  return df


def remove_abandoned_accounts(df):
  start_time = 1704056400 # 01.01.2024 00:00:00
  print('Abandoned accounts found: ' + str(df[df.last_seen_time < start_time].id.count()))
  df.drop(df[df.last_seen_time < start_time].index, inplace=True)
  if df[df.last_seen_time < start_time].id.count() == 0:
    print('Abandoned accounts was removed')
  else:
    print('Abandoned accounts was not removed')
  return df


def remove_large_freinds(df):
    print('Large friends accounts found: ' + str(df[df.friends_count > 5000].id.count()))
    df.drop(df[df.friends_count > 5000].index, inplace=True)
    if str(df[df.friends_count > 5000].id.count()) == 0:
        print('Large friends accounts was removed')
    else:
        print('Large friends accounts was not removed')
    return df


def handle_duplicates(df):
  aggregation_parameters = {
      'bdate': 'first',
      'career': 'first',
      'city': 'first',
      'friends_count': 'first',
      'last_seen_platform': 'first',
      'occupation': 'first',
      'political': 'first',
      'langs': 'first',
      'sex': 'first',
      'university': 'first',
      'verified': 'first',
      'connection_type': lambda x: list(x),
      'group_type': lambda x: list(x),
      'friends_ids': 'first'
  }
  df = df.groupby('id').agg(aggregation_parameters).reset_index()
  print('Duplicates aggregated')
  return df


def fill_none_values(df):
  values = {
      'bdate': '01.01.1900',
      'career': 'none',
      'city': 'unknown',
      'friends_count': 0,
      'last_seen_platform': 0,
      'occupation': 'none',
      'political': 0,
      'langs': 'unknown',
      'university': 'none'
  }
  df.fillna(value=values, inplace=True)
  
  def set_bdate_default(bdate):
    parts = bdate.split('.')
    if len(parts) == 2:
      return '01.01.1900'
    return bdate

  df['bdate'] = df['bdate'].apply(set_bdate_default)
  return df
  
def fix_date_issue(df):
    def correct_invalid_dates(date_str):
        day, month, year = date_str.split('.')
    
        if day == '31' and month == '2':
            corrected_date = f'2.3.{year}'
            return corrected_date
        elif day == '30' and month == '2':
            corrected_date = f'1.3.{year}'
            return corrected_date
        elif day == '29' and month == '2':
            corrected_date = f'1.3.{year}'
            return corrected_date
        elif day == '31' and month == '4':
            corrected_date = f'29.4.{year}'
            return corrected_date
        else:
            return date_str
    df['bdate'] = df['bdate'].apply(correct_invalid_dates)
    return df


def datatypes_normalization(df):
  int_columns = ['id', 'last_seen_platform', 'political', 'sex', 'verified']
  category_columns = ['city', 'occupation', 'university']
  
  df[int_columns] = df[int_columns].astype('int')
  df['bdate'] = pd.to_datetime(df['bdate'], format='%d.%m.%Y', dayfirst=True, errors='raise')
  #print(df[df['bdate'].isnull()])
  df[category_columns] = df[category_columns].astype('category')
  print('data normalization done')
  return df


def extract_friends(df):
    #friends_ids_df = df[['friends_ids']]
    #friends_ids_df.loc[:, 'friends_ids'] = friends_ids_df['friends_ids'].apply(ast.literal_eval)
    df = df[['friends_ids']]
    df['friends_ids'] = df['friends_ids'].apply(json.loads)
    print('json loaded')
    df = df.explode('friends_ids').dropna(subset=['friends_ids']).drop_duplicates(subset=['friends_ids'])
    return(df)


def main():
  df = combine_files()
  df = remove_closed_accounts(df)
  df = remove_abandoned_accounts(df)
  df = remove_large_freinds(df)
  df = handle_duplicates(df)
  df = fill_none_values(df)
  df = fix_date_issue(df)
  df = datatypes_normalization(df)
  df.to_parquet(path='dataset.parquet', engine='fastparquet')
