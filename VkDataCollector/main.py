import csv
import classes


def main():
    print('Worker start')
    with open(f'VkDataCollector/group_list.csv', 'r') as group_list_file:
        group_list = csv.DictReader(group_list_file)
        for group_data in group_list:
            group = classes.Groups(group_data['group_id'], group_data['group_type'])
            group.get_group_basic_info()
            group.get_members_list()
            print('Group parsing has been finished')
    print('Worker end')
        

main()