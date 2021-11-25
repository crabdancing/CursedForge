#!/bin/env python3
# Copyleft (C) Alexandria Pettit 2021, GNU GPLv3
# The main body of our program. iterates through URLs, extracting the project ID and then downloading

# TODO: add click-powered console UI? Need to dust off my old skills with that library.

# TODO: add actual downloading functionality

# TODO: add ability to generate curseforge-formatted manifest.json modpack file
# TODO: See: https://github.com/PistolRcks/curseforge-mass-downloader/wiki/Structuring-manifest.json
# TODO: add thing to make sure we're getting 'text only version' to prevent parsing errors
# TODO: detect consistent Google 404 page (e.g., broken link)
# TODO: detect when Google tries to fake us out with a fake 404 page (wait a bit, then reload)
# TODO: abstract out ADT for 'parser that reads project ID number', implement in dedicated class
# TODO: build class for parsing Yahoo instead of Google (should result in separating the load and reducing captchas and other problems...)

# https://webcache.googleusercontent.com/search?q=cache:https%3A//www.curseforge.com/minecraft/texture-packs/classic-3d&strip=1&vwsrc=0
import logging
from pathlib import Path
from typing import List

from lib import ProjectIDFinder, SimpleLogger
from lib.SimpleLogger import stream_handler, file_handler
from lib.Id2NameDB_CSV import ID2NameDB


class Main:
    projectIDFinder = None
    url_list: List[str] = []
    db = ID2NameDB()
    logger = logging.getLogger(__name__)
    results = open('results-ids.txt', 'w')

    def __init__(self, log_handlers: List):
        for log_handler in log_handlers:
            self.logger.addHandler(log_handler)
        self.logger.info('Getting IDs from URLs...')

    def load_modlist(self):
        line: str
        for line in open('modlist.conf').readlines():
            line = line.strip()
            if line == '' or line[0] in (';', '#'):
                continue
            self.url_list.append(line)

    def scrape_from_curseforge_website(self, curse_url) -> int:
        # ProjectIDFinder is expensive and annoying to run.
        # it requires running a patched chromium driver and opening GUI
        # We only want to load this if we absolutely have to.
        if not self.projectIDFinder:
            self.projectIDFinder = ProjectIDFinder.ProjectIDFinder([stream_handler, file_handler])
        return self.projectIDFinder.send_request(curse_url)

    def process_urls(self):
        for curse_url in self.url_list:
            project_name: str = Path(curse_url).stem
            self.logger.info('Processing URL:', curse_url)
            # Try to grab ID from cache db
            project_id: int = self.db.query_project_id(project_name)
            # If that failed, resort to scraping
            if not project_id:
                self.logger.info(f'Couldn\'t find project name in local DB: {project_name}')
                project_id = self.scrape_from_curseforge_website(curse_url)
            # Hopefully THAT worked, right?
            if project_id:
                self.db.set_project_id(project_id, project_name)
                self.results.write(str(project_id) + '\n')
            else:  # Oh well... :S
                self.logger.warning(f'Failed to extract project ID for link: {curse_url}')
                continue

            self.db.commit()

    def main(self):
        self.load_modlist()
        self.process_urls()
        self.db.commit()


main = Main([SimpleLogger.stream_handler, SimpleLogger.file_handler])

if __name__ == '__main__':
    main.main()
