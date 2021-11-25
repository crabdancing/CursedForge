# Copyleft (C) Alexandria Pettit 2021, GNU GPLv3
# This code bypasses both the obnoxious Cloudfare protection and most of the page bloat
# by querying Google cache for CurseForge project pages.
# It then extracts the project ID, which can be used for automating downloads and whatever else.

import random
import re
import time
from pathlib import Path

#  Selenium webdriver imports
from typing import List

import undetected_chromedriver.v2 as uc
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import logging
import urllib.parse


class ProjectIDFinder:
    google_cache: str = 'https://webcache.googleusercontent.com/search?q=cache:'
    url_prefix = google_cache
    url_suffix = '&strip=1&vwsrc=0'
    project_id: int = ''
    driver = None
    uses_google_cache: bool = True
    pattern = re.compile(r'<span>Project ID</span>\W*<span>(\d*)</span>')
    options = uc.ChromeOptions()
    logger = logging.getLogger(__name__)

    # user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0'

    def __init__(self, log_handlers: List[logging.StreamHandler] = None, default_profile_name: Path = Path('cursedforge-chromium'), options=None):

        for log_handler in log_handlers:
            self.logger.addHandler(log_handler)
        if options:
            self.options = options
        else:
            # set options to default
            user_data_dir: Path = Path.home() / '.config' / default_profile_name
            self.options.add_argument(f'--user-data-dir={user_data_dir}')
            self.options.add_argument("--disable-gpu")
            # self.options.add_argument('--window-size=1400,2100')
            # self.options.add_argument('--user-agent="{self.user_agent}"')
        self.driver = uc.Chrome(options=options)

    def has_curseforge_page_loaded(self):
        return 'CurseForge' in self.driver.title

    def randomize_window(self):
        """ Minimizes detectability by shifting window dimensions around. """
        self.driver.set_window_rect(50 * random.random(), 50 * random.random(), 100 * random.random() + 1024,
                                    100 * random.random() + 768)

    def get_id_via_regex(self):
        search = self.pattern.search(self.driver.page_source)
        if search:
            self.project_id = int(search.group(1))
            self.logger.info(f'Mod ID: {self.project_id}')
        else:
            self.logger.info('No match :(')

    def send_request(self, curseforge_url: str):

        self.driver.get(self.url_prefix + urllib.parse.quote(curseforge_url) + self.url_suffix)

        # polling technique is cool, but seems to somehow trip up Cloudfare's anti-bot detection
        # wait = WebDriverWait(driver, 100, poll_frequency=2)
        # wait.until(scan_stupidly)

        while not self.has_curseforge_page_loaded():
            time.sleep(1)
        if self.uses_google_cache:
            return self.get_id_google_cache()
        else:
            return self.get_id_no_google_cache()

    def get_id_google_cache(self):
        for element in self.driver.find_elements(By.XPATH, "//div[@class='w-full flex justify-between']"):
            self.logger.info(f'Processing element: {element.text}')
            if 'Project ID' in str(element.text):
                try:
                    # for some reason it shows up as 'Project ID [id number]' instead of the number by itself
                    project_id_text = str(element.text)
                    project_id = project_id_text.split(' ')[2]
                    return int(project_id.strip())
                except (IndexError, ValueError):
                    self.logger.exception('Has site changed?')
                return None  # none return indicates some error happened

    def get_id_no_google_cache(self):
        # What we're looking for here is:
        #  <div class="w-full flex justify-between">
        #  <span>Project ID</span>
        #
        #  <span>320215</span></div>
        expecting_project_id = False
        for element in self.driver.find_elements(By.XPATH, "//div[@class='w-full flex justify-between']"):
            self.logger.info(f'Processing element:{element.text}')
            if 'Project ID' in str(element.text):
                expecting_project_id = True
            if expecting_project_id:
                try:
                    # for some reason it shows up as 'Project ID\n [id number]' instead of the number by itself
                    return int(element.text.split('\n')[1].strip())
                except (IndexError, ValueError):
                    self.logger.exception('Has site changed?')
                return None  # none return indicates some error happened
