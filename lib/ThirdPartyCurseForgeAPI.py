# Copyleft (C) Alexandria Pettit 2021, GNU GPLv3
# Some wrapper methods for easily using a third-party CurseForge API instance,
# (such as the curse.nikky.moe one)
import logging
from symtable import Function
from typing import List, Union, Optional

import requests
import requests_cache
import re

from lib import SimpleLogger


class ThirdPartyCurseForgeAPI:
    """ Can access a third party CurseForge API to retrieve details.
    Uses request_cache so that it's not too rude when running lots of tests or re-building modpack. """

    def __init__(self, target_loader_name='Forge', target_game_version='1.16.5',
                 target_game_version_regex='1.16.*', cache_expire_time: int = 86400, log_handlers=None):
        self.logger = logging.getLogger(__name__)


        # cache_expire_time -- number of seconds before dumping old cache. Is set to 1 day by default.

        # pretty sure `install_cache` won't actually apply outside of our module & class scope here,
        # but I haven't bothered to actually check :S
        requests_cache.install_cache(cache_name='curse_forge_api_cache',
                                     backend='sqlite', expire_after=cache_expire_time)
        # A list of version matching methods in descending order of strictness
        self.match_methods: List[()] = [self.match_strict, self.match_normal, self.match_lax]
        self.target_loader_name = target_loader_name
        self.target_game_version = target_game_version
        self.target_game_version_regex = target_game_version_regex

    def get_dl_link(self, my_project_id: str,
                    target_game_version_glob='1.16*') -> Optional[str]:
        # for examples of what this looks like:
        # https://curse.nikky.moe/api/addon/377282/files
        r = requests.get(f'https://curse.nikky.moe/api/addon/{my_project_id}/files')
        dl_items = r.json()
        # We iterate over match methods so that we try strict on all first, then we can try normal on all, then try lax.
        # If we did it the other way, we'd settle for the first thing found with a lax method,
        # even if there was a better match further down the `dl_items` list...
        for match_method in self.match_methods:
            for dl_item in dl_items:
                self.logger.debug(f'Download info item in JSON: {dl_item}')
                if match_method(dl_item):
                    dl_url: str = dl_item['downloadUrl']
                    self.logger.info(f'Download URL found: {dl_url}')
                    return dl_url
        self.logger.info(f'Warning! Couldn\'t download {my_project_id}')
        return None

    def match_strict(self, dl_item) -> bool:
        """ Attempts strict match of game/loader version. """
        # may be compatible with multiple versions, hence this API choice
        game_versions: List[str] = dl_item['gameVersion']
        matches_game_version: bool = self.target_game_version in game_versions
        matches_loader: bool = self.target_loader_name in game_versions  # I've seen 'Forge' vs 'Fabric' in list before
        return matches_loader and matches_game_version  # verbose but readable

    def match_normal(self, dl_item) -> bool:
        """ Attempts exact match. Many projects on CurseForge have no loader specified in their metadata. """
        game_versions: List[str] = dl_item['gameVersion']
        matches_game_version: bool = self.target_game_version in game_versions
        return matches_game_version

    def match_lax(self, dl_item) -> bool:
        """ Attempts regex match. Many projects on CurseForge have no loader specified in their metadata. """
        game_versions: List[str] = dl_item['gameVersion']
        for game_version in game_versions:
            match = re.match(self.target_game_version_regex, game_version)
            if match is not None:
                return True
        # we cycled through all -- regex must not match any :')
        return False

