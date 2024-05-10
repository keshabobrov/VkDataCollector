import variables
import requests
import json


class Groups:
    def __init__(self, group_id) -> None:
        self.group_id = group_id
        self.name = None
        self.members_count = None
        self.is_verified = None
        self.type = None
    
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
        self.members_count = json_response['response']['groups'][0]['members_count']
        self.name = json_response['response']['groups'][0]['name']
        self.is_verified = json_response['response']['groups'][0]['verified']
        self.type = json_response['response']['groups'][0]['type']
    
    def get_members_list(self):
        offset = 0
        members_list = []
        api_method = 'groups.getMembers'
        get_members_list_request ={
            'access_token': variables.token,
            'group_id': self.group_id,
            'v': variables.version
        }
        while offset < self.members_count:
            get_members_list = f"{variables.url}/{api_method}"
            get_members_list_request['offset'] = offset
            response = requests.post(get_members_list, get_members_list_request)
            json_response = json.loads(response.text)
            members_list.append(json_response['response']['items'])
            offset += 1000
        return members_list