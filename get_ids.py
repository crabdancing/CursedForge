#!/bin/env python3

# https://webcache.googleusercontent.com/search?q=cache:https%3A//www.curseforge.com/minecraft/texture-packs/classic-3d&strip=1&vwsrc=0
import logging
from pathlib import Path
from typing import List

from lib import SimpleLogger
from lib.Id2NameDB_CSV import ID2NameDB
from lib.ProjectIDFinder import ProjectIDFinder


class MainGetIDs:
    projectIDFinder = None
    url_list: List[str] = []
    db = ID2NameDB()
    ids: List[str] = []

    def __init__(self):
        self.logger = logging.getLogger(__name__)
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
            self.projectIDFinder = ProjectIDFinder()
        return self.projectIDFinder.send_request(curse_url)

    def process_urls(self):
        for curse_url in self.url_list:
            project_name: str = Path(curse_url).stem
            self.logger.info(f'Processing URL: {curse_url}')
            # Try to grab ID from cache db
            project_id: int = self.db.query_project_id(project_name)
            # If that failed, resort to scraping
            if not project_id:
                self.logger.info(f'Couldn\'t find project name in local DB: {project_name}')
                project_id = self.scrape_from_curseforge_website(curse_url)
            # Hopefully THAT worked, right?
            if project_id:
                self.db.set_project_id(project_id, project_name)
                self.ids.append(str(project_id) + '\n')
            else:  # Oh well... :S
                self.logger.warning(f'Failed to extract project ID for link: {curse_url}')
                continue

            self.db.commit()

    def main(self):
        print('Getting mod IDs...')
        self.load_modlist()
        self.process_urls()
        self.db.commit()

        open('results-ids.txt', 'w').writelines(self.ids)
        print('Done.')


main = MainGetIDs()

if __name__ == '__main__':
    main.main()
