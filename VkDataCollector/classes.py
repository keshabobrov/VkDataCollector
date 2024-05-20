import variables
import requests
import json
import csv
import os
import time
import logging

logging.basicConfig(filename='logger.log', level=logging.ERROR, filemode='w')

class Groups:
    def __init__(self, group_id, group_type) -> None:
        self.group_id = group_id
        self.name = None
        self.members_count = None
        self.is_verified = None
        self.group_type = group_type
    
    def get_group_basic_info(self):
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
    
    def get_members_list(self):
        # Getting a 1000 members id's and providing them to get_user_info function for further parsing
        # Repeating until last thousand will be processed
        try:
            offset = 0
            members_list = []
            api_method = 'groups.getMembers'
            get_members_list_request ={
                'access_token': variables.token,
                'group_id': self.group_id,
                'v': variables.version
            }
            while offset < self.members_count:
                print(str(offset) + ' ----- ' + self.name)
                get_members_list = f"{variables.url}/{api_method}"
                get_members_list_request['offset'] = offset
                time.sleep(0.15)
                response = requests.post(get_members_list, get_members_list_request)
                json_response = json.loads(response.text)
                members_list.append(json_response['response']['items'])
                get_user_info(','.join(map(str,json_response['response']['items'])), self.name, self.group_type)
                offset += 1000
            return members_list
        except:
            logging.error(f'Error in get_members_list: {json_response}', exc_info=True)


class Users:
    def __init__(self) -> None:
        self.id = None
        self.is_closed = None
        self.bdate = None
        self.career = None
        self.city = None
        self.friends_count = 1
        self.education = None
        self.last_seen_time = None
        self.last_seen_platform = None
        self.occupation_type = None
        self.personal_political = None
        self.personal_langs = None
        self.personal_religion = None
        self.sex = None
        self.university_name = None
        self.verified = None
        self.connection_type = None
        self.group_type = None
        self.friends = None
        
    def attr_to_list(self):
        # Adding all class attributes to list for further csv saving
        attr_list = []
        attr_list.extend([self.id, self.is_closed, self.bdate, self.career, self.city, self.friends_count, self.education])
        attr_list.extend([self.last_seen_time, self.last_seen_platform, self.occupation_type, self.personal_political, self.personal_langs])
        attr_list.extend([self.personal_religion, self.sex, self.university_name, self.verified, self.connection_type, self.group_type, self.friends])
        return(attr_list)
    
    def get_friends(self):
        try:
            offset = 0
            friends_list = []
            api_method = 'friends.get'
            get_friends_list_request ={
                'access_token': variables.token,
                'user_id': self.id,
                'v': variables.version
            }
            while offset < self.friends_count:
                get_friends_list = f"{variables.url}/{api_method}"
                get_friends_list_request['offset'] = offset
                time.sleep(0.15)
                response = requests.post(get_friends_list, get_friends_list_request)
                json_response = json.loads(response.text)
                if not self.is_closed:
                    self.friends_count = json_response['response']['count']
                    friends_list.append(json_response['response']['items'])
                offset += 5000
            self.friends = friends_list
        except:
            logging.error(f'Error in get_friends: {json_response}', exc_info=True)
        
        
def get_user_info(user_ids, group_name, group_type):
    try:
        api_method = 'users.get'
        get_users_request ={
            'access_token': variables.token,
            'user_ids': user_ids,
            'v': variables.version,
            'fields': 'bdate, career, city, education, friends_count, sex, verified, last_seen, occupation, personal, universities'
        }
        time.sleep(0.15)
        response = requests.post(f"{variables.url}/{api_method}", get_users_request)
        json_response = json.loads(response.text)['response']
        for data_string in json_response:
            user_data = Users()
            user_data.id = data_string.get('id')
            user_data.is_closed = data_string.get('is_closed')
            user_data.bdate = data_string.get('bdate')
            user_data.city = data_string.get('city', {}).get('title')
            user_data.education = data_string.get('education', {}).get('university_name')
            user_data.last_seen_time = data_string.get('last_seen', {}).get('time')
            user_data.last_seen_platform = data_string.get('last_seen', {}).get('platform')
            user_data.occupation_type = data_string.get('occupation', {}).get('type')
            user_data.personal_political = data_string.get('personal', {}).get('political')
            user_data.personal_religion = data_string.get('personal', {}).get('religion')
            user_data.sex = data_string.get('sex')
            user_data.verified = data_string.get('verified')
            user_data.connection_type = group_name
            user_data.group_type = group_type
            # Multiple data fields parsing. Universities:
            if 'universities' in data_string:
                uni_name_list = []
                for uni in data_string['universities']:
                    uni_name_list.append(uni['name'])
                user_data.university_name = uni_name_list
            # Languages:
            if 'personal' in data_string and 'langs' in data_string['personal']:
                langs_list = []
                for lang in data_string['personal']['langs']:
                    langs_list.append(lang)
                user_data.personal_langs = langs_list
            # Career:
            if 'career' in data_string:
                career_list = []
                for job in data_string['career']:
                    if 'position' in job:
                        career_list.append(job['position'])
                user_data.career = career_list
            user_data.get_friends()
            attr_list = user_data.attr_to_list()
            # Writing to file
            with open(f'VkDataCollector/datasets/{group_name}.csv', 'a') as csv_file:
                writer = csv.writer(csv_file)
                headers = ['id', 'is_closed', 'bdate', 'career', 'city', 'friends_count', 'education', 'last_seen_time',
                            'last_seen_platform', 'occupation', 'political', 'langs', 'religion', 'sex', 'university', 'verified', 
                            'connection_type', 'group_type', 'friends_ids']
                if os.stat(f'VkDataCollector/datasets/{group_name}.csv').st_size == 0:
                    writer.writerow(headers)
                writer.writerow(attr_list)
    except:
        logging.error(f'Error in get_user_info: {json_response}', exc_info=True)