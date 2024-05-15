import csv
import classes


def main():
    print('Worker start')
    with open(f'group_list.csv', 'r') as group_list_file:
        group_list = csv.reader(group_list_file, delimiter='\n')
        for group_id in group_list:
            group = classes.Groups(group_id)
            group.get_group_basic_info()
            members_list = group.get_members_list()
            with open(f'datasets/{group.name}.csv', 'w') as csv_file:
                writer = csv.writer(csv_file, delimiter='\n')
                writer.writerows(members_list)
                print('written file')
    print('Worker end')
        

main()