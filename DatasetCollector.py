import requests
import json
import os
import csv
import time
from dotenv import load_dotenv
import variables


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
        'access_token': variables.token,
        'group_id': group_id,
        'v': variables.version
    }
    while offset < members_count:
        get_members_list = f"{variables.url}/{method}"
        get_members_list_request['offset'] = offset
        response = requests.post(get_members_list, get_members_list_request)
        json_response = json.loads(response.text)
        members_list.append(json_response['response']['items'])
        offset += 1000
    return(members_list)
