import requests
import variables
import logging
import time
import json
import csv

logging.basicConfig(filename='logger.log', level=logging.WARNING, filemode='w')

def reader():
    chunk_size = 25
    with open('../datasets/friends.csv', 'r') as user_ids_file:
        chunk_data = []
        for row in user_ids_file:
            if row[:-1] == 'friends_ids': continue
            chunk_data.append(row[:-1]) # Appending without \n
            if len(chunk_data) == chunk_size:
                yield chunk_data 
                chunk_data  = []
        if chunk_data : yield chunk_data  # yield chunk if there is remaining values


def backend_executor(ids):
    try:
        while True:
            request = {
                'access_token': variables.token,
                'v': variables.version,
                'code': f'var id_list = {ids};'
                        'var current_index = 0;'
                        'var results = [];'
                        'while (current_index < id_list.length) {'
                            'var friends_list = API.friends.get({"user_id": id_list[current_index]});'
                            'results.push({'
                                '"user_id": id_list[current_index],'
                                '"friends": friends_list.items'
                            '});'
                            'current_index = current_index + 1;'
                        '};'
                        'return results;'
            }
            response = requests.post(f"{variables.url}/execute", request)
            json_response = json.loads(response.text)
            if 'error' in json_response and json_response['error']['error_code'] == 6:
                logging.warning(f'Too many requests. Retrying...')
                time.sleep(0.05)
                continue
            return json_response
    except:
       logging.error(f'Some error happend ----- {json_response}', exc_info=True)
       variables.bot.send_message(variables.telegram_watcher_id, 'Some error!')
       time.sleep(60)


def data_processor():
    variables.bot.send_message(variables.telegram_watcher_id, 'Worker starter')
    index = 0
    file_number = 0
    for chunk in reader():
        if index == 250000:
            file_number += 1
            variables.bot.send_message(variables.telegram_watcher_id, f'Another done — {file_number}')
            index = 0
        with open(f'datasets/{file_number}.csv', 'a') as fl:
            headers = ['user_id', 'friends']
            writer = csv.DictWriter(fl, fieldnames=headers)
            output = backend_executor(chunk)
            for row in output['response']:
                writer.writerow(row)
        index += 25
