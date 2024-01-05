import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import activity as act
from garmin_util import get_activities_path

def create_weekly_kilometers_dataframe(activities: list[act.Activity], year: int) -> pd.DataFrame:
    activities_running_sorted: list[act.Activity] = sorted(
        filter(
            lambda a: a.get_start_time_gmt().year == year,
            activities
        ),
        key = lambda a: a.get_start_time_gmt(),
        reverse = True
    )

    columns = ['Week', 'Values']

    current_week = ''
    current_sum = 0.0
    dfs_to_concat = []
    for a in activities_running_sorted:
        week_number = a.get_start_time_gmt().strftime("%W")
        activity_week = f'{a.get_start_time_gmt().year}-{week_number}'

        if current_week != activity_week and current_sum > 0:
            new_data = [current_week, current_sum / 100000]
            dfs_to_concat.append(pd.DataFrame([new_data], columns=columns))

            current_sum = 0

        current_week = activity_week
        current_sum = current_sum + a.distance_centimeters

    df_weeks = pd.concat(dfs_to_concat, ignore_index=True)
    df_weeks = df_weeks.sort_values(by='Week')

    return df_weeks


if len(sys.argv) != 5 and len(sys.argv) != 4:
    print('Error: this script requires three arguments.')
    print('Usage: summarize_activities.py /path/to/garmin-data <user_mail> <year>')
    print('Usage: summarize_activities.py /path/to/garmin-data <user_mail> <year> /path/to/output.png')
    exit(-1)

input_garmin_data_path = sys.argv[1]
user_mail = sys.argv[2]
input_year=sys.argv[3]
output_path = None
if len(sys.argv) ==5:
    output_path = sys.argv[4]

path_activities = get_activities_path(input_garmin_data_path, user_mail)

df = create_weekly_kilometers_dataframe(act.load_activities(path_activities, 'running'), int(input_year))

"""
plt.figure(figsize=(8, 6))  # Optional: Set the figure size

# Create the bar chart
plt.bar(df['Week'], df['Values'])
# plt.bar(df.head(20)['Week'], df.head(20)['Values'])

# Add labels and a title
plt.xlabel('Week')
plt.ylabel('Kilometers')
plt.title('Weekly kilometers')
"""

sns.set(style="whitegrid")

plt.figure(figsize=(12, 8))

custom_palette = sns.color_palette(["#3498db", "#e74c3c", "#2ecc71"])
sns.set_palette(custom_palette)

sns.barplot(x='Week', y='Values', data=df, hue='Values',  dodge=False)

average_value = df['Values'].mean()
plt.axhline(y=average_value, color='gray', linestyle='--', label='Average Value')

plt.xlabel('Week', fontsize=12)
plt.ylabel('Kilometers', fontsize=12)
plt.title(f'Weekly kilometers in {input_year}', fontsize=14)

plt.legend().set_visible(False)
plt.xticks(rotation=45, fontsize=10)

if output_path is not None:
    plt.savefig(output_path)
else:
    plt.show()
