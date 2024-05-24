import pandas as pd
import os
import glob


def combine_files():
  path = '../datasets'
  files = glob.glob(os.path.join(path , "*.csv"))
  li = []

  for file in files:
    print(file)
    filepath = path + file
    frame = pd.read_csv(filepath)
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


def datatypes_normalization(df):
  int_columns = ['id', 'last_seen_platform', 'political', 'sex', 'verified']
  category_columns = ['city', 'occupation', 'university']
  
  df[int_columns] = df[int_columns].astype('int')
  df['bdate'] = pd.to_datetime(df['bdate'], format='%d.%m.%Y', errors='raise')
  df[category_columns] = df[category_columns].astype('category')
  print('data normalization done')
  return df


def main():
  df = combine_files()
  df = remove_closed_accounts(df)
  df = remove_abandoned_accounts(df)
  df = handle_duplicates(df)
  df = fill_none_values(df)
  df = datatypes_normalization(df)
  df.to_parquet(path='dataset.parquet')


main()
