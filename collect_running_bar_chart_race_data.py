import csv
import sys
import activity as act
import gear
from garmin_util import get_activities_path, get_gears_path

if len(sys.argv) != 4 and len(sys.argv) != 5:
    print('Error: this script requires three arguments.')
    print('Usage: collect.py /path/to/garmin-data <user_mail> /path/to/output.csv')
    print('Usage: collect.py /path/to/garmin-data <user_mail> /path/to/output.csv <years>')
    exit(-1)

input_garmin_data_path = sys.argv[1]
user_mail = sys.argv[2]
output_path = sys.argv[3]
years: list[int] = []
if len(sys.argv) == 5:
    years = list(map(int, sys.argv[4].split(';')))

path_activities = get_activities_path(input_garmin_data_path, user_mail)
path_gears = get_gears_path(input_garmin_data_path, user_mail)

activities = act.load_activities(path_activities, 'running')
gears = gear.load_gears(path_gears)
activity_to_gear = gear.load_activity_to_gear(path_gears)

activities_running_sorted = sorted(
    filter(lambda a: a.get_id() in activity_to_gear, activities),
    key = lambda a: a.get_start_time_gmt()
)

gears_accumulator_dict = {}

for gear in gears.values():
    gears_accumulator_dict[gear] = 0.0

summary = [['date', *map(lambda g: g.get_gear_name(), gears.values())]]

for a in activities_running_sorted:
    activity_gear = gears[activity_to_gear[a.get_id()]]
    gears_accumulator_dict[activity_gear] = gears_accumulator_dict[activity_gear] + a.get_distance()
    if len(years) == 0 or a.get_start_time_gmt().year in years:
        summary.append([a.get_start_time_gmt(), *map(gears_accumulator_dict.get, gears.values())])

with open(output_path, 'w', encoding='utf8') as destFile:
    writer = csv.writer(destFile)
    writer.writerows(summary)
