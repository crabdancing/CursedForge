# Copyleft (C) Alexandria Pettit 2021, GNU GPLv3
# Some wrapper methods for easily using a third-party CurseForge API instance,
# (such as the curse.nikky.moe one)

import requests


def get_dl_link(my_project_id, loader_name='Fabric', game_version='1.17.1'):
    r = requests.get(f'https://curse.nikky.moe/api/addon/{my_project_id}')
    json = r.json()
    # for examples of what this looks like:
    # https://curse.nikky.moe/api/addon/377282
    latest_files_section = json['latestFiles']
    for item in latest_files_section:
        if loader_name in item['gameVersion'] and game_version in item['gameVersion']:
            return item['downloadUrl']
    return None
