import csv
import datasetCollector
import classes


id = 171147949
group_name = 'Редакция'


def main():
    print('Worker start')
    group = classes.Groups(id)
    group.get_group_basic_info()
    members_list = datasetCollector.get_members_list(group.group_id, group.group_members_count)
    with open(f'datasets/{group_name}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter='\n')
        writer.writerows(members_list)
        print('Worker end')
        

main()