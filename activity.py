from datetime import datetime
import json

from garmin_util import get_activities_paths


class Activity:
    def __init__(self, activity_id: str, type: str, sport_type: str, distance_centimeters: float, start_time_gmt: datetime):
        self.activity_id = activity_id
        self.type = type
        self.sport_type = sport_type
        self.distance_centimeters = distance_centimeters
        self.start_time_gmt = start_time_gmt

    @staticmethod
    def from_garmin_json(activity_json: str) -> 'Activity':
        return Activity(
            activity_json['activityId'],
            activity_json['activityType'],
            activity_json['sportType'],
            activity_json['distance'],
            datetime.fromtimestamp(activity_json['startTimeGmt'] / 1000.0)
        )

    def get_id(self) -> str:
        return self.activity_id

    def get_type(self) -> str:
        return self.type

    def get_sport_type(self) -> str:
        return self.sport_type

    def get_start_time_gmt(self) -> datetime:
        return self.start_time_gmt
    
    def get_distance(self) -> float:
        return self.distance_centimeters

    def __repr__(self) -> str:
        return f'[Activity ID: {self.activity_id}] {self.type} {self.sport_type} {self.distance_centimeters} (centimeters) on {self.start_time_gmt}'


class Activities:

    def __init__(self, garmin_data_path: str, user_mail: str):
        self.garmin_data_path = garmin_data_path
        self.user_mail = user_mail
    
    def load_activities(self, activity_types: list[str] = []) -> list[Activity]:
        paths = get_activities_paths(self.garmin_data_path, self.user_mail)
        activities = []
        
        for path in paths:
            activities.extend(self._load_activities(path, activity_types))
        
        return activities

    def _load_activities(self, activities_json_path: str, activity_types: list[str] = []) -> list[Activity]:
        activities_json = json.load(open(activities_json_path))

        activities = []

        for activity_json in activities_json[0]['summarizedActivitiesExport']:
            activities.append(Activity.from_garmin_json(activity_json))

        if len(activity_types) > 0:
            activities = list(filter(
                lambda a: a.get_type() in activity_types,
                activities
            ))

        return activities



def load_activities(activities_json_path: str, activity_types: list[str] = []) -> list[Activity]:
    activities_json = json.load(open(activities_json_path))

    activities = []

    for activity_json in activities_json[0]['summarizedActivitiesExport']:
        activities.append(Activity.from_garmin_json(activity_json))

    if len(activity_types) > 0:
        activities = list(filter(
            lambda a: a.get_type() in activity_types,
            activities
        ))

    return activities


if __name__ == '__main__':
    PATH_ACTIVITIES_TEST = 'garmin-data/0227bb72-be08-421e-afdf-6904c4483c30_1/'

    activities = Activities(PATH_ACTIVITIES_TEST, 'hlfzeus@gmail.com')

    activities_list = activities.load_activities(['running', 'treadmill_running'])
    if activities_list:
        longest_activity = max(activities_list, key=lambda a: a.get_distance())
        print(f'The activity with the longest length is: {longest_activity}')
    else:
        print('No activities found.')
