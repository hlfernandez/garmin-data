import activity as act
import gear as gear
import csv
import sys

if len(sys.argv) != 4:
    print('Error: this script requires three arguments.')
    print('Usage: collect.py /path/to/garmin-data <user_mail> /path/to/output.csv')
    exit(-1)

input_garmin_data_path = sys.argv[1]
user_mail = sys.argv[2]
output_path = sys.argv[3]

# FILE_ACTIVITIES_TEST = 'Garmin/edfe2951-1fdd-4cd4-ae3f-e9f62023e00d_1/DI_CONNECT/DI-Connect-Fitness/hlfzeus@gmail.com_0_summarizedActivities.json'
FILE_ACTIVITIES_TEST = '{}/DI_CONNECT/DI-Connect-Fitness/{}_0_summarizedActivities.json'.format(input_garmin_data_path, user_mail)

activities = act.load_activities(FILE_ACTIVITIES_TEST)
for a in activities:
    print(a)

# FILE_GEARS_TEST = 'Garmin/edfe2951-1fdd-4cd4-ae3f-e9f62023e00d_1/DI_CONNECT/DI-Connect-Fitness/hlfzeus@gmail.com_gear.json'
FILE_GEARS_TEST = '{}/DI_CONNECT/DI-Connect-Fitness/{}_gear.json'.format(input_garmin_data_path, user_mail)

gears = gear.load_gears(FILE_GEARS_TEST)
activity_to_gear = gear.load_activity_to_gear(FILE_GEARS_TEST)

activities_running_sorted = sorted(
    filter(
        lambda a: a.get_type() == 'running',
        filter(lambda a: a.get_id() in activity_to_gear, activities)
    ),
    key = lambda a: a.get_start_time_gmt()
)

gears_accumulator_dict = {}

for gear in gears.values():
    gears_accumulator_dict[gear] = 0

print(gears_accumulator_dict)

summary = [['date', *map(lambda g: g.get_gear_name(), gears.values())]]

for a in activities_running_sorted:
    activity_gear = gears[activity_to_gear[a.get_id()]]
    gears_accumulator_dict[activity_gear] = gears_accumulator_dict[activity_gear] + a.get_distance()
    summary.append([a.get_start_time_gmt(), *map(lambda g: gears_accumulator_dict.get(g), gears.values())])

print(summary[len(summary)-1])
print(gears_accumulator_dict)

with open(output_path, 'w') as destFile:
    writer = csv.writer(destFile)
    writer.writerows(summary)
