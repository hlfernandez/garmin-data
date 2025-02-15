import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import activity as act
from garmin_util import get_activities_path

def create_run_lengh_dist_dataframe(activities: list[act.Activity]) -> pd.DataFrame:
    lengths = []
    for a in activities:
        lengths.append(a.get_distance() / 100000)

    return pd.DataFrame({ 'Lengths' : lengths})


if len(sys.argv) != 4 and len(sys.argv) != 3:
    print('Error: this script requires three arguments.')
    print('Usage: run_length_distribution.py /path/to/garmin-data <user_mail>')
    print('Usage: run_length_distribution.py /path/to/garmin-data <user_mail> /path/to/output.png')
    exit(-1)

input_garmin_data_path = sys.argv[1]
user_mail = sys.argv[2]
output_path = None
if len(sys.argv) ==4:
    output_path = sys.argv[3]

activities = act.Activities(input_garmin_data_path, user_mail)

df = create_run_lengh_dist_dataframe(
    activities.load_activities(['running', 'treadmill_running', 'trail_running'])
)

bin_edges = [0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40, 42.5, 45]

"""
# Basic plot
plt.figure(figsize=(8, 6))
df['Lengths'].plot.hist(bins=bin_edges, edgecolor='black')

plt.xlabel('Length (kilometers)')
plt.ylabel('Frequency')
plt.title('Histogram of run lengths')

plt.show()
"""

sns.set(style="whitegrid")

plt.figure(figsize=(10, 6))

ax = sns.histplot(data=df, x='Lengths', bins=bin_edges, kde=False, edgecolor='black', color='skyblue')

plt.xlabel('Length (kilometers)', fontsize=14)
plt.ylabel('Number of runs', fontsize=14)

total_count = len(df['Lengths'])
plt.title(f'Histogram of run lengths ({total_count})', fontsize=16)

ax.grid(axis='y', linestyle='--', alpha=0.7)

for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='baseline', fontsize=10, color='black')

if output_path is not None:
    plt.savefig(output_path)
else:
    plt.show()
