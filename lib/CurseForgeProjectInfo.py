# Copyleft (C) Alexandria Pettit 2021 GNU GPLv3
# A basic layer to abstract away and make neater accessing information from our json responses

from typing import Iterable


class CurseForgeFileInfo:
    json: dict

    def __init__(self, json: dict):
        self.json = json

    @property
    def id_num(self):
        return self.json['id']

    @property
    def download_url(self):
        return self.json['downloadUrl']

    @property
    def date(self):
        return self.json['fileDate']

    @property
    def iter_game_versions(self) -> Iterable[str]:
        for version in self.json['gameVersion']:
            yield version


class CurseForgeProjectInfo:
    json: dict

    def __init__(self, json: dict):
        self.json = json

    @property
    def slug(self):
        return self.json['slug']

    @property
    def id_num(self):
        return self.json['id']

    @property
    def summary(self):
        return self.json['summary']

    def iter_latest_files(self) -> Iterable[CurseForgeFileInfo]:
        """
        Iterates over files in our project info, giving us
        """
        # for examples of what this looks like:
        # https://curse.nikky.moe/api/addon/377282
        latest_files_section = self.json['latestFiles']

        for section in latest_files_section:
            yield CurseForgeFileInfo(section)
