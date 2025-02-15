import glob

def get_activities_path(input_garmin_data_path: str, user_mail: str) -> str:
    return f'{input_garmin_data_path}/DI_CONNECT/DI-Connect-Fitness/{user_mail}_0_summarizedActivities.json'

def get_activities_paths(input_garmin_data_path: str, user_mail: str) -> list[str]:
    pattern = f'{input_garmin_data_path}/DI_CONNECT/DI-Connect-Fitness/{user_mail}_*_summarizedActivities.json'
    return glob.glob(pattern)

def get_gears_path(input_garmin_data_path: str, user_mail: str) -> str:
    return f'{input_garmin_data_path}/DI_CONNECT/DI-Connect-Fitness/{user_mail}_gear.json'

