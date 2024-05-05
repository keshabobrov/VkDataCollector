import requests
import json
import os
import csv
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path = '.env')
token = os.getenv('VK_API_SERVICE_TOKEN')
version = os.getenv('VK_API_VERSION')
url = os.getenv('URL')

id = 171147949
group_name = 'Редакция'


def get_members_count(group_id):
    """
        Get the total number of members in a VK group.

        Args:
            group_id (long): The ID of the VK group.

        Returns:
            int: The total number of members in the group.
    """
    method = 'groups.getById'
    get_members_count_request ={
            'access_token': token,
            'group_id': id,
            'v': version,
            'fields': 'members_count'
        }
    response = requests.post(f"{url}/{method}", get_members_count_request)
    json_response = json.loads(response.text)
    members_count = json_response['response']['groups'][0]['members_count']
    return members_count


def get_members_list(group_id, members_count):
    """
        Get a list of members of a VK group.

        Args:
            group_id (long): The ID of the VK group.
            members_count (int): The total number of members in the group.

        Returns:
            list: A list containing the members of the group.
    """
    offset = 0
    members_list = []
    method = 'groups.getMembers'
    get_members_list_request ={
        'access_token': token,
        'group_id': group_id,
        'v': version
    }
    while offset < members_count:
        get_members_list = f"{url}/{method}"
        get_members_list_request['offset'] = offset
        response = requests.post(get_members_list, get_members_list_request)
        json_response = json.loads(response.text)
        members_list.append(json_response['response']['items'])
        offset += 1000
    return(members_list)
        

def main():
    members_count = get_members_count(id)
    members_list = get_members_list(id, members_count)
    with open(f'Datasets/{group_name}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter='\n')
        writer.writerows(members_list)
        

main()