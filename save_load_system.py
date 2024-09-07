# PhysicsEngineAndLevelEditor is a 2D physics engine and level editor
# in python, using pygame and pymunk, and rendering through openGL

# Copyright (C) 2024  Emmet Schell

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# this program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# To contact the author of this program, Email them at
# emmetschell@gmail.com.

import os.path
import json
from PymunkPhysicsAndLevels import objects

def save_to_json(room, key, list):
    with open(os.path.join('PymunkPhysicsAndLevels', 'LevelData', str(room)), 'r+') as file:
        try:
            data = json.load(file)
            data.update({key: list})
            file.seek(0)
            json.dump(data, file)
        except json.decoder.JSONDecodeError:
            data = {key: list}
            json.dump(data, file)


def load_from_json(room):
    with open(os.path.join('PymunkPhysicsAndLevels', 'LevelData', str(room)), 'r+') as file:
        level_dict = json.load(file)
        return level_dict


def save_object(room, class_object, parameter_list):
    with open(os.path.join('PymunkPhysicsAndLevels', 'LevelData', str(room)), 'r+') as keys:
        try:
            keys_dict = json.load(keys)
            save_to_json(room, key=str(int(list(keys_dict)[-1]) + 1), list=[str(class_object), *parameter_list])
        except json.decoder.JSONDecodeError:
            save_to_json(room, key=str(1), list=[str(class_object), *parameter_list])


def load_level(room):
    level_dict = load_from_json(room)
    object_dict = {}
    for i in level_dict.keys():
        object_type = level_dict[i][0]
        class_caller = getattr(objects, str(object_type))
        object_dict[f'{i}'] = class_caller(*level_dict[i][1:])
    return object_dict
