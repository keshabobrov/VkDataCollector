import variables
import requests
import json


class Groups:
    def __init__(self, group_id) -> None:
        self.group_id = group_id
        self.group_name = None
        self.group_members_count = None
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
        self.group_members_count = json_response['response']['groups'][0]['members_count']
        self.group_name = json_response['response']['groups'][0]['name']
        self.is_verified = json_response['response']['groups'][0]['verified']
        self.type = json_response['response']['groups'][0]['type']