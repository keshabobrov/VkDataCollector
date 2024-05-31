import vk_execute
import collect_friends
import csv

    
def collect_user_data():
    print('Worker start')
    with open(f'group_list.csv', 'r') as group_list_file:
       group_list = csv.DictReader(group_list_file)
       for group_data in group_list:
            group = vk_execute.Groups(group_data['group_id'], group_data['group_type'])
            group.get_group_basic_info()
            group.get_members_list()
            group.file.close()
            print('Group parsing has been finished')
    print('Worker finished')


def collect_friends_list():
    print('Worker start')
    collect_friends.data_processor()
    print('Worker ended')
        

collect_friends_list()