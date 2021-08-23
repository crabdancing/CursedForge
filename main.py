#!/bin/env python3
# Copyleft (C) Alexandria Pettit 2021, GNU GPLv3
# The main body of our program. iterates through URLs, extracting the project ID and then downloading

# TODO: add ability to import mod links from .txt file list of URLs

# TODO: add squlite for storing mappings between project names and IDs, so that we don't make redundant requests

# TODO: add click-powered console UI? Need to dust off my old skills with that library.

# TODO: add actual downloading functionality

# TODO: add ability to generate curseforge-formatted manifest.json modpack file
# TODO: See: https://github.com/PistolRcks/curseforge-mass-downloader/wiki/Structuring-manifest.json

import ProjectIDFinder
import ThirdPartyCurseForgeAPI

from SimpleLogger import root_logger, stream_handler, file_handler

projectIDFinder = ProjectIDFinder.ProjectIDFinder([stream_handler, file_handler])
tests = ['https://www.curseforge.com/minecraft/mc-mods/adorn',
         'https://www.curseforge.com/minecraft/mc-mods/stonevaults-dungeons-towers']

for curse_url in tests:
    print('Processing URL:', curse_url)
    project_id = projectIDFinder.send_request(curse_url)
    if project_id:
        result = ThirdPartyCurseForgeAPI.get_dl_link(project_id)
    else:
        root_logger.warning(f'Failed to extract project ID for link: {curse_url}')
        continue
    if result:
        print(result)
    else:
        root_logger.warning(f'Failed to find download link via third-party API for link: {curse_url}')
        continue
