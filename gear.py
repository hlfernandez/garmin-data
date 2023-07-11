import json


class Gear:
    def __init__(self, gear_id: str, custom_make_model: str, display_name: str = ''):
        self.gear_id = gear_id
        self.custom_make_model = custom_make_model
        self.display_name = display_name
        if self.display_name is not '':
            if self.display_name == self.custom_make_model:
                self.gear_name = self.display_name
            else:
                self.gear_name = f'{self.custom_make_model} ({self.display_name})'
        else:
            self.gear_name = self.custom_make_model

    @staticmethod
    def from_garmin_json(garmin_gear_json: str) -> 'Gear':
        if 'displayName' in garmin_gear_json:
            return Gear(garmin_gear_json['gearPk'], garmin_gear_json['customMakeModel'], garmin_gear_json['displayName'])
        
        return Gear(garmin_gear_json['gearPk'], garmin_gear_json['customMakeModel'])

    def get_id(self) -> str:
        return self.gear_id
    
    def get_gear_name(self) -> str:
        return self.gear_name

    def __repr__(self):
        return f'[Gear ID: {self.gear_id}] {self.gear_name}'

    def __hash__(self):
        return hash(self.gear_id)

    def __eq__(self, other):
        return self.gear_id == other.gear_id


def load_gears(gear_json_path: str):
    gears_json = json.load(open(gear_json_path))

    gears = {}

    for gear_json in gears_json[0]['gearDTOS']:
        new_gear = Gear.from_garmin_json(gear_json)
        gears[new_gear.get_id()] = new_gear

    return gears


def load_activity_to_gear(gear_json_path: str):
    gears_json = json.load(open(gear_json_path))
    toret = {}

    for gear_id in gears_json[0]['gearActivityDTOs']:
        for gear_activity in gears_json[0]['gearActivityDTOs'][gear_id]:
            toret[gear_activity['activityId']] = gear_activity['gearPk']

    return toret


if __name__ == '__main__':
    FILE_GEARS_TEST = 'Garmin/edfe2951-1fdd-4cd4-ae3f-e9f62023e00d_1/DI_CONNECT/DI-Connect-Fitness/hlfzeus@gmail.com_gear.json'

    for gear in load_gears(FILE_GEARS_TEST).values():
        print(gear)

    print(load_activity_to_gear(FILE_GEARS_TEST))
