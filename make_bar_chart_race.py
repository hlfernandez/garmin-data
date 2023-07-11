import bar_chart_race as bcr
import pandas as pd
import sys

if len(sys.argv) != 3:
    print('Error: this script requires two arguments.')
    print('Usage: make_bar_chart_race.py /path/to/data.csv /path/to/output.mp4')
    exit(-1)

input_data = sys.argv[1]
oputput = sys.argv[2]

gears_data = pd.read_csv(input_data)
gears_data.set_index('date', drop=True, inplace=True)
gears_data.drop(columns=gears_data.columns[gears_data.sum()==0], inplace=True)
gears_data = gears_data.divide(100000, axis='columns')

bcr.bar_chart_race(
    df=gears_data,
    steps_per_period=1,
    title='Running shoes usage',
    orientation='h',
    sort='desc',
    interpolate_period=False,
    filename=oputput
)
