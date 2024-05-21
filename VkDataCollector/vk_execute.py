import requests
import variables
import logging
import json
import csv
import os
import time

logging.basicConfig(filename='logger.log', level=logging.WARNING, filemode='w')

class Groups:
    def __init__(self, group_id, group_type) -> None:
        self.group_id = group_id
        self.name = None
        self.members_count = None
        self.is_verified = None
        self.group_type = group_type
        self.file = None
    
    def get_group_basic_info(self):
        try:
            api_method = 'groups.getById'
            request ={
                'access_token': variables.token,
                'group_id': self.group_id,
                'v': variables.version,
                'fields': 'members_count, verified'
            }
            response = requests.post(f"{variables.url}/{api_method}", request)
            json_response = json.loads(response.text)
            # Fetching basic group info
            self.members_count = json_response['response']['groups'][0]['members_count']
            self.name = json_response['response']['groups'][0]['name']
            self.is_verified = json_response['response']['groups'][0]['verified']
            self.file = open(f'datasets/{self.name}.csv', 'a')
            self.writer = csv.writer(self.file)
            headers = ['id', 'is_closed', 'bdate', 'career', 'city', 'friends_count', 'last_seen_time', 'last_seen_platform',
                    'occupation', 'political', 'langs', 'religion', 'sex', 'university', 'verified', 'connection_type', 'group_type', 'friends_ids']
            if os.stat(f'datasets/{self.name}.csv').st_size == 0:
                self.writer.writerow(headers)
        except:
            logging.error(json_response)
    
    def get_members_list(self):
        try:
            offset = 0
            logging.warning(f'Started ————— {self.name}')
            while offset < self.members_count:
                request = {
                    'access_token': variables.token,
                    'v': variables.version,
                    'code': f'var members_list = API.groups.getMembers({{"group_id":{self.group_id}, "offset":{offset}, "count":15}});'
                            'var users_data = API.users.get({'
                                '"user_ids": members_list.items,'
                                '"fields": "bdate, career, city, education, friends_count, sex, verified, last_seen, occupation, personal, universities"'
                                '});'
                            'var current_num = 0;'
                            'var total_num = members_list.items.length;'
                            'var results = [];'
                            'while (current_num < total_num) {'
                                'var friend_list = null;'
                                'var latest_career = 0;'
                                'var latest_university = 0;'
                                'if (users_data[current_num].career.length > 0) {'
                                    'latest_career = users_data[current_num].career.length - 1;'
                                '};'
                                'if (users_data[current_num].universities.length > 0) {'
                                    'latest_university = users_data[current_num].universities.length - 1;'
                                '};'
                                'if (users_data[current_num].is_closed == false) {'
                                    'friend_list = API.friends.get({"user_id": users_data[current_num].id}).items;'
                                '};'
                                'results.push({'
                                    '"id": users_data[current_num].id,'
                                    '"is_closed": users_data[current_num].is_closed,'
                                    '"bdate": users_data[current_num].bdate,'
                                    '"career": users_data[current_num].career[latest_career]["position"],'
                                    '"city": users_data[current_num].city["title"],'
                                    '"friends_count": friend_list.length,'
                                    '"last_seen_time": users_data[current_num].last_seen["time"],'
                                    '"last_seen_platform": users_data[current_num].last_seen["platform"],'
                                    '"occupation_type": users_data[current_num].occupation["type"],'
                                    '"personal_political": users_data[current_num].personal["political"],'
                                    '"personal_langs": users_data[current_num].personal["langs"],'
                                    '"personal_religion": users_data[current_num].personal["religion"],'
                                    '"sex": users_data[current_num].sex,'
                                    '"university_name": users_data[current_num].universities[latest_university]["name"],'
                                    '"verified": users_data[current_num].verified,'
                                    '"friends": friend_list'
                                '});'
                                'current_num = current_num + 1;'
                            '};'
                            'return results;'
                }
                time.sleep(0.06)
                response = requests.post(f"{variables.url}/execute", request)
                json_response = json.loads(response.text)
                write_file(json_response, self.name, self.group_type, self.writer)
                offset += 15
        except:
            logging.error(json_response)


def data_processing(row, group_name, group_type):
    user_data = []
    user_data.append(row['id'])
    user_data.append(row['is_closed'])
    user_data.append(row['bdate'])
    user_data.append(row['career'])
    user_data.append(row['city'])
    user_data.append(row['friends_count'])
    user_data.append(row['last_seen_time'])
    user_data.append(row['last_seen_platform'])
    user_data.append(row['occupation_type'])
    user_data.append(row['personal_political'])
    user_data.append(row['personal_langs'])
    user_data.append(row['personal_religion'])
    user_data.append(row['sex'])
    user_data.append(row['university_name'])
    user_data.append(row['verified'])
    user_data.append(group_name)
    user_data.append(group_type)
    user_data.append(row['friends'])
    return user_data


def write_file(response, group_name, group_type, writer):
    for row in response['response']:
        user_data = data_processing(row, group_name, group_type)
        writer.writerow(user_data)
