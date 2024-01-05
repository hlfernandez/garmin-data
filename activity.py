from datetime import datetime
import json


class Activity:
    def __init__(self, activity_id: str, type: str, distance_centimeters: float, start_time_gmt: datetime):
        self.activity_id = activity_id
        self.type = type
        self.distance_centimeters = distance_centimeters
        self.start_time_gmt = start_time_gmt

    @staticmethod
    def from_garmin_json(activity_json: str) -> 'Activity':
        return Activity(
            activity_json['activityId'],
            activity_json['activityType'],
            activity_json['distance'],
            datetime.fromtimestamp(activity_json['startTimeGmt'] / 1000.0)
        )

    def get_id(self) -> str:
        return self.activity_id

    def get_type(self) -> str:
        return self.type

    def get_start_time_gmt(self) -> datetime:
        return self.start_time_gmt
    
    def get_distance(self) -> float:
        return self.distance_centimeters

    def __repr__(self) -> str:
        return f'[Activity ID: {self.activity_id}] {self.type} {self.distance_centimeters} (centimeters) on {self.start_time_gmt}'


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
    FILE_ACTIVITIES_TEST = 'garmin-data/edfe2951-1fdd-4cd4-ae3f-e9f62023e00d_1/DI_CONNECT/DI-Connect-Fitness/hlfzeus@gmail.com_0_summarizedActivities.json'

    activities_test  = load_activities(FILE_ACTIVITIES_TEST)

    for a in activities_test:
        print(a)
