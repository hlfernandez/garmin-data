import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import activity as act
from garmin_util import get_activities_path
from datetime import datetime, timedelta

def create_daily_kilometers_dataframe(activities: list[act.Activity], start_date: str, end_date: str) -> pd.DataFrame:
    # Create a DataFrame with all the dates in the specified range
    date_range = pd.date_range(start=start_date, end=end_date)
    df_days = pd.DataFrame(date_range, columns=['Date'])
    df_days['Kilometers'] = 0.0

    # Sum the activities distances to the corresponding day
    for a in activities:
        activity_date = a.get_start_time_gmt().date()
        if start_date <= activity_date.strftime("%Y-%m-%d") <= end_date:
            df_days.loc[df_days['Date'] == pd.to_datetime(activity_date), 'Kilometers'] += a.distance_centimeters / 100000.0

    # Calculate the rolling sum of the last 7 days (including the current day)
    df_days['7-Day Sum'] = df_days['Kilometers'].rolling(window=7, min_periods=1).sum()

    # Identify days where the 7-day sum is more than 10% higher than the previous day
    df_days['Increase > 10%'] = df_days['7-Day Sum'] > df_days['7-Day Sum'].shift(1) * 1.1

    return df_days

def parse_date_range(date_arg: str):
    if date_arg.startswith("year="):
        year = int(date_arg.split("=")[1])
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
    elif date_arg.startswith("range="):
        date_range = date_arg.split("=")[1]
        start_date, end_date = date_range.split("_")
    else:
        raise ValueError("Invalid date argument. Use 'year=<year>' or 'range=<from>_<to>'")
    
    return start_date, end_date

if len(sys.argv) != 5 and len(sys.argv) != 4:
    print('Error: this script requires three arguments.')
    print('Usage: summarize_activities.py /path/to/garmin-data <user_mail> year=<year>')
    print('Usage: summarize_activities.py /path/to/garmin-data <user_mail> range=<from>_<to>')
    print('Usage: summarize_activities.py /path/to/garmin-data <user_mail> year=<year> /path/to/output.png')
    print('Usage: summarize_activities.py /path/to/garmin-data <user_mail> range=<from>_<to> /path/to/output.png')
    exit(-1)

input_garmin_data_path = sys.argv[1]
user_mail = sys.argv[2]
date_arg = sys.argv[3]
output_path = None
if len(sys.argv) == 5:
    output_path = sys.argv[4]

# Parse date range or year
start_date, end_date = parse_date_range(date_arg)

activities = act.Activities(input_garmin_data_path, user_mail)

df = create_daily_kilometers_dataframe(
    activities.load_activities(['running', 'treadmill_running', 'trail_running']),
    start_date,
    end_date
)

sns.set(style="whitegrid")

plt.figure(figsize=(12, 8))

custom_palette = sns.color_palette(["#3498db", "#e74c3c", "#2ecc71"])
sns.set_palette(custom_palette)

# Plot the 7-day rolling sum
sns.lineplot(x='Date', y='7-Day Sum', data=df, label='7-Day Sum')

# Highlight days where the increase is more than 10%
highlight_df = df[df['Increase > 10%'] == True]
sns.scatterplot(x='Date', y='7-Day Sum', data=highlight_df, color='red', label='> 10% Increase')

average_value = df['7-Day Sum'].mean()
plt.axhline(y=average_value, color='gray', linestyle='--', label='Average Value')

plt.xlabel('Date', fontsize=12)
plt.ylabel('7-Day Kilometers Sum', fontsize=12)
plt.title(f'7-Day Rolling Sum of Kilometers ({start_date} to {end_date})', fontsize=14)

plt.legend()
plt.xticks(rotation=45, fontsize=10)

if output_path is not None:
    plt.savefig(output_path)
else:
    plt.show()
